from jose import jwt

from openid_connect import connect_url
from openid_connect._verify import verify
from openid_connect.errors import BadRequest, NotImplemented


class RelyingParty:
	def __init__(self):
		self.providers = {}

	def add_provider(self, client):
		if isinstance(client, str):
			client = connect_url(client)

		self.providers[client.issuer] = client

	def verify(self, id_token = '', iss = '', **params):
		if id_token:
			try:
				iss = jwt.get_unverified_claims(id_token).get('iss', '')
			except jwt.JWTError as e:
				raise BadRequest("Invalid ID token.")

			# Work around Google bug
			if iss == 'accounts.google.com':
				iss = 'https://accounts.google.com'

		if not iss:
			raise BadRequest("Missing id_token/iss parameter.")

		try:
			client = self.providers[iss]
		except KeyError as e:
			raise NotImplemented("Unsupported issuer.") from None

		return client.verify(id_token = id_token, iss = iss, **params)
