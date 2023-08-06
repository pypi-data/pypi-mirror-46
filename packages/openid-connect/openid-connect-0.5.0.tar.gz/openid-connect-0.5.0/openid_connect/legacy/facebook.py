from openid_connect.legacy._oauth2 import OAuth2Client


class Client(OAuth2Client):
	def __init__(self, url = 'https://facebook.com', client_id = None, client_secret = None):
		super().__init__(url, client_id, client_secret)

	def get_configuration(self):
		return dict(
			issuer = self.url,
			userinfo_endpoint = 'https://graph.facebook.com/me?fields=email',
			response_types_supported = [],
			subject_types_supported = ["public"],
			token_endpoint_auth_methods_supported = [],
		)

	def translate_userinfo(self, data):
		return dict(
			sub = data['id'],
			email = data['email'],
		)
