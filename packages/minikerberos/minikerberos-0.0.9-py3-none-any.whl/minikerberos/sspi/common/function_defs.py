from .defines import *
import enum
import datetime
import ctypes

# call API to get max token size, or..
maxtoken = 2880 # bytes

_FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
def FiletimeToDateTime(ft):
	timestamp = (ft.dwHighDateTime << 32) + ft.dwLowDateTime
	print(timestamp)
	return _FILETIME_null_date + datetime.timedelta(microseconds=timestamp/10)

#timestamp is LARGE_INTEGER
#same as FILETIME structure

#https://docs.microsoft.com/en-us/windows/desktop/api/minwinbase/ns-minwinbase-filetime
class FILETIME(Structure):
	_fields_ = [
		("dwLowDateTime",   DWORD),
		("dwHighDateTime",   DWORD),
	]
PFILETIME = POINTER(FILETIME)
TimeStamp = FILETIME
PTimeStamp = PFILETIME

SEC_CHAR = CHAR
PSEC_CHAR = PCHAR

class LUID(Structure):
	_fields_ = [
		("LowPart",	 DWORD),
		("HighPart",	LONG),
	]

PLUID = POINTER(LUID)

# https://github.com/benjimin/pywebcorp/blob/master/pywebcorp/ctypes_sspi.py
class SecHandle(Structure): 
	
	_fields_ = [('dwLower',POINTER(ULONG)),('dwUpper',POINTER(ULONG))]
	def __init__(self): # populate deeply (empty memory fields) rather than shallow null POINTERs.
		super(Structure, self).__init__(byref(ULONG()), byref(ULONG()))

class SecBuffer(Structure):
	"""Stores a memory buffer: size, type-flag, and POINTER. 
	The type can be empty (0) or token (2).
	InitializeSecurityContext will write to the buffer that is flagged "token"
	and update the size, or else fail 0x80090321=SEC_E_BUFFER_TOO_SMALL."""	
	_fields_ = [('cbBuffer',ULONG),('BufferType',ULONG),('pvBuffer',PVOID)]
	def __init__(self, token=maxtoken):
		buf = ctypes.create_string_buffer(token) 
		Structure.__init__(self,sizeof(buf),2,ctypes.cast(byref(buf),PVOID))
	@property
	def Buffer(self):
		return ctypes.string_at(self.pvBuffer, size=self.cbBuffer)	 
	
class SecBufferDesc(Structure):
	"""Descriptor stores SECBUFFER_VERSION=0, number of buffers (e.g. one),
	and POINTER to an array of SecBuffer structs."""
	_fields_ = [('ulVersion',ULONG),('cBuffers',ULONG),('pBuffers',POINTER(SecBuffer))]
	def __init__(self, *args):
		Structure.__init__(self,0,1,byref(SecBuffer(*args)))
	def __getitem__(self, index):
		return self.pBuffers[index]
PSecBufferDesc = POINTER(SecBufferDesc)

PSecHandle = POINTER(SecHandle)
CredHandle = SecHandle
PCredHandle = PSecHandle
CtxtHandle = SecHandle
PCtxtHandle = PSecHandle


# https://apidock.com/ruby/Win32/SSPI/SSPIResult
class SEC_E(enum.Enum):
	OK = 0x00000000 
	CONTINUE_NEEDED = 0x00090312 
	INSUFFICIENT_MEMORY = 0x80090300 #There is not enough memory available to complete the requested action.
	INTERNAL_ERROR = 0x80090304 #An error occurred that did not map to an SSPI error code.
	INVALID_HANDLE = 0x80090301
	INVALID_TOKEN = 0x80090308
	LOGON_DENIED = 0x8009030C
	NO_AUTHENTICATING_AUTHORITY = 0x80090311
	NO_CREDENTIALS = 0x8009030E #No credentials are available in the security package.
	TARGET_UNKNOWN = 0x80090303
	UNSUPPORTED_FUNCTION = 0x80090302
	WRONG_PRINCIPAL = 0x80090322
	NOT_OWNER = 0x80090306 #The caller of the function does not have the necessary credentials.
	SECPKG_NOT_FOUND = 0x80090305 #The requested security package does not exist.
	UNKNOWN_CREDENTIALS = 0x8009030D #The credentials supplied to the package were not recognized.
	#SEC_I
	RENEGOTIATE = 590625
	COMPLETE_AND_CONTINUE = 590612
	COMPLETE_NEEDED = 590611
	INCOMPLETE_CREDENTIALS = 590624

class SECPKG_CRED(enum.IntFlag):
	AUTOLOGON_RESTRICTED = 0x00000010 	#The security does not use default logon credentials or credentials from Credential Manager.
										#This value is supported only by the Negotiate security package.
										#Windows Server 2008, Windows Vista, Windows Server 2003 and Windows XP:  This value is not supported.

	BOTH = 3							#Validate an incoming credential or use a local credential to prepare an outgoing token. This flag enables both other flags. This flag is not valid with the Digest and Schannel SSPs.
	INBOUND = 1							#Validate an incoming server credential. Inbound credentials might be validated by using an authenticating authority when InitializeSecurityContext (General) or AcceptSecurityContext (General) is called. If such an authority is not available, the function will fail and return SEC_E_NO_AUTHENTICATING_AUTHORITY. Validation is package specific.
	OUTBOUND = 2						#Allow a local client credential to prepare an outgoing token.
	PROCESS_POLICY_ONLY = 0x00000020 	#The function processes server policy and returns SEC_E_NO_CREDENTIALS, indicating that the application should prompt for credentials.
										#This value is supported only by the Negotiate security package.
										#Windows Server 2008, Windows Vista, Windows Server 2003 and Windows XP:  This value is not supported.

class DecryptFlags(enum.Enum):										
	SIGN_ONLY = 0
	SECQOP_WRAP_NO_ENCRYPT = 2147483649 # same as KERB_WRAP_NO_ENCRYPT

#https://github.com/mhammond/pywin32/blob/d64fac8d7bda2cb1d81e2c9366daf99e802e327f/win32/Lib/sspi.py#L108
#https://docs.microsoft.com/en-us/windows/desktop/secauthn/using-sspi-with-a-windows-sockets-client
#https://msdn.microsoft.com/en-us/library/Aa374712(v=VS.85).aspx
def AcquireCredentialsHandle(client_name, package_name, tragetspn, cred_usage, pluid = None, authdata = None):
	def errc(result, func, arguments):
		if SEC_E(result) == SEC_E.OK:
			return result
		raise Exception('%s failed with error code %s (%s)' % ('AcquireCredentialsHandle', result, SEC_E(result)))
		
	_AcquireCredentialsHandle = windll.Secur32.AcquireCredentialsHandleA
	_AcquireCredentialsHandle.argtypes = [PSEC_CHAR, PSEC_CHAR, ULONG, PLUID, PVOID, PVOID, PVOID, PCredHandle, PTimeStamp]
	_AcquireCredentialsHandle.restype  = DWORD
	_AcquireCredentialsHandle.errcheck  = errc
	
	#TODO: package_name might be different from version to version. implement functionality to poll it properly!
	
	cn = None
	if client_name:
		cn = LPSTR(client_name.encode('ascii'))
	pn = LPSTR(package_name.encode('ascii'))
	
	creds = CredHandle()
	ts = TimeStamp()
	res = _AcquireCredentialsHandle(cn, pn, cred_usage, pluid, authdata, None, None, byref(creds), byref(ts))
	return creds
	
# https://msdn.microsoft.com/en-us/library/windows/desktop/aa375507(v=vs.85).aspx
def InitializeSecurityContext(creds, target, ctx = None, flags = 0, TargetDataRep  = 0, token = None):
	def errc(result, func, arguments):
		if SEC_E(result) in [SEC_E.OK, SEC_E.COMPLETE_AND_CONTINUE,SEC_E.COMPLETE_NEEDED,SEC_E.CONTINUE_NEEDED,SEC_E.INCOMPLETE_CREDENTIALS]:
			return result
		raise Exception('%s failed with error code %s (%s)' % ('InitializeSecurityContext', result, SEC_E(result)))
		
	_InitializeSecurityContext = windll.Secur32.InitializeSecurityContextA
	_InitializeSecurityContext.argtypes = [PCredHandle, PCtxtHandle, PSEC_CHAR, ULONG, ULONG, ULONG, PSecBufferDesc, ULONG, PCtxtHandle, PSecBufferDesc, PULONG, PTimeStamp]
	_InitializeSecurityContext.restype  = DWORD
	_InitializeSecurityContext.errcheck  = errc
	
	ptarget = LPSTR(target.encode('ascii'))
	newbuf = SecBufferDesc()
	outputflags = ULONG()
	expiry = TimeStamp()
	
	if token:
		token = SecBufferDesc(token)
	
	if not ctx:
		ctx = CtxtHandle()
		res = _InitializeSecurityContext(byref(creds), None, ptarget, flags, 0 ,TargetDataRep, byref(token) if token else None, 0, byref(ctx), byref(newbuf), byref(outputflags), byref(expiry))
	else:
		res = _InitializeSecurityContext(byref(creds), byref(ctx), ptarget, flags, 0 ,TargetDataRep, byref(token) if token else None, 0, byref(ctx), byref(newbuf), byref(outputflags), byref(expiry))
	
	return res, ctx, newbuf, outputflags, expiry
	
def DecryptMessage(ctx, data, message_no = 0):
	def errc(result, func, arguments):
		if SEC_E(result) == SEC_E.OK:
			return result
		raise Exception('%s failed with error code %s (%s)' % ('DecryptMessage', result, SEC_E(result)))
		
	_DecryptMessage = windll.Secur32.DecryptMessage
	_DecryptMessage.argtypes = [PCtxtHandle, PSecBufferDesc, ULONG, ULONG]
	_DecryptMessage.restype  = DWORD
	_DecryptMessage.errcheck  = errc
	
	data = SecBufferDesc(data)
	flags = ULONG()

	res = _DecryptMessage(byref(ctx), byref(data), message_no, byref(flags))
	
	return data
	
if __name__ == '__main__':
	creds = None
	#target = 'krbtgt@TEST'
	#target = 'srv_http@TEST.corp'
	target = 'WIN2019AD@test.corp'
	
	creds = AcquireCredentialsHandle(None, 'KERBEROS', target, SECPKG_CRED.BOTH)
	print(creds)
	res, ctx, newbuf, outputflags, expiry = InitializeSecurityContext(creds, target)
	for i in range(newbuf.cBuffers):
		print(newbuf[i].Buffer)

"""
	 ss = AcquireCredentialsHandle (
			NULL, 
			lpPackageName,
			SECPKG_CRED_OUTBOUND,
			NULL, 
			NULL, 
			NULL, 
			NULL, 
			hCred,
			&Lifetime);
			
	self.credentials_expiry=win32security.AcquireCredentialsHandle(
				client_name, self.pkg_info['Name'],
				sspicon.SECPKG_CRED_OUTBOUND,
None, auth_info)
"""