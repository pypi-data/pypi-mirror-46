class Error(Exception):
	pass


class BadRequest(Error):
	code = 400


class Forbidden(Error):
	code = 403


class NotImplemented(Error):
	code = 501
