from time import time

from jose import jws

from openid_connect._verify import verify

DEFAULT_ALG = {
	'EC': 'ES256',
	'RSA': 'PS256',
	'oct': 'HS256',
}


class Provider:
	def __init__(self, issuer, *, key = None):
		self.issuer = issuer
		self.client_id = issuer
		self.key = key

	@property
	def keys(self):
		return dict(keys = [self.key])

	def issue(self, data, lifetime, *, aud = None):
		now = time()

		return jws.sign(
			dict(
				**data,
				iss = self.issuer,
				aud = aud or self.client_id,
				iat = now,
				exp = now + lifetime.total_seconds(),
			),
			self.key,
			algorithm = self.key.get('alg', DEFAULT_ALG[self.key['kty']]),
		)

	verify = verify
