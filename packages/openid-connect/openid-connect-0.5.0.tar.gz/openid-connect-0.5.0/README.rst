openid-connect - Low-level Python OIDC Client library
=====================================================
.. image:: https://badge.fury.io/py/openid-connect.svg
	:target: https://badge.fury.io/py/openid-connect

This is a low-level Python library for authentication against OpenID
Providers (e.g. Google).

For high-level libraries see the Aiakos_ project.

What is OpenID Connect?
-----------------------

It's a OAuth2-based standard for authentication in applications.

Legacy authorization servers
----------------------------

openid-connect does also support some legacy OAuth2 providers
that do not implement OpenID Connect protocol:

- facebook
- gitlab
- github

For gitlab and github - both official and on-premise instances are supported.

Requirements
------------

- Python 3.7+ - might work on older 3.x versions, but it's not tested
- python-jose_

.. _Aiakos: https://gitlab.com/aiakos
.. _python-jose: https://github.com/mpdavis/python-jose
