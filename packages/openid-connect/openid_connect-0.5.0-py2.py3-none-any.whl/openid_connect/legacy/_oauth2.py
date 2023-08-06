from openid_connect._oidc import OpenIDClient
from openid_connect.errors import BadRequest, Forbidden, NotImplemented

from requests.exceptions import HTTPError


class OAuth2Client(OpenIDClient):
	def verify(self, token_type = '', access_token = '', **params):
		if not token_type:
			raise BadRequest("Missing token_type parameter.")
		if token_type.lower() != 'bearer':
			raise NotImplemented("Unsupported token type.")

		if not access_token:
			raise BadRequest("Missing access_token parameter.")

		try:
			data = self.get_userinfo(access_token)
		except HTTPError as e:
			if e.response.status_code == 401:
				raise Forbidden("Provider did not accept given access token.") from e
			raise

		return dict(
			iss = self.issuer,
			**data,
		)
