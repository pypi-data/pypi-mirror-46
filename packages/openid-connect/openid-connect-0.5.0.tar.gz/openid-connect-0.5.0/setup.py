#!/usr/bin/env python3

from setuptools import setup

with open('README.rst') as f:
	readme = f.read()

setup(
	name = "openid-connect",
	version = "0.5.0",
	description = "Low-level Python OIDC Client library",
	long_description = readme,
	author = "Aiakos Contributors",
	author_email = "aiakos@aiakosauth.com",
	url = "https://gitlab.com/aiakos/python-openid-connect",
	keywords = "auth oauth openid oidc social ldap",

	install_requires = [
		'python-jose',
		'requests',
	],

	packages = ["openid_connect", "openid_connect.legacy"],
	zip_safe = True,

	license = "MIT",
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: MIT License',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7',
		'Topic :: System :: Systems Administration :: Authentication/Directory',
	],
)
