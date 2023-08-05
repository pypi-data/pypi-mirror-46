import enum
from minikerberos.sspi.common.function_defs import *
from minikerberos.asn1_structs import *

class SSPIResult(enum.Enum):
	OK = 'OK'
	CONTINUE = 'CONT'
	ERR = 'ERR'

class KerberosSSPI:
	def __init__(self, target, client_name = None):
		self.client_name = client_name
		self.target = target
		
		#self.creds = AcquireCredentialsHandle(self.client_name, 'KERBEROS', self.target, SECPKG_CRED.BOTH)
		self.creds = AcquireCredentialsHandle(self.client_name, 'NEGOTIATE', self.target, SECPKG_CRED.BOTH)
		self.ctx = None
	
	def init_ctx(self, in_token = None):
		res, self.ctx, newbuf, outputflags, expiry = InitializeSecurityContext(self.creds, self.target, token = in_token, ctx = self.ctx)
		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print(res)
		if res == SEC_E.OK:
			return SSPIResult.OK, newbuf[0].Buffer
		else:
			return SSPIResult.CONTINUE, newbuf[0].Buffer
		
	def wrap(self, data):
		return None
		
		
	def unwrap(self, data):
		res, dec_data = DecryptMessage(self.ctx, data, message_no = 0)
		return dec_data[0].Buffer