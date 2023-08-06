from jose import jwt

from openid_connect.errors import Forbidden


def verify(client, id_token, **params):
	try:
		data = jwt.decode(
			id_token,
			client.keys,
			audience = client.client_id,
			options = dict(
				verify_iss = False,
				verify_at_hash = False,
			),
		)
	except jwt.JWTError as e:
		raise Forbidden("Invalid ID token.") from e

	# Work around Google bug
	if data['iss'] == 'accounts.google.com':
		data['iss'] = 'https://accounts.google.com'

	if data['iss'] != client.issuer:
		raise Forbidden("Invalid ID token.")

	return data
