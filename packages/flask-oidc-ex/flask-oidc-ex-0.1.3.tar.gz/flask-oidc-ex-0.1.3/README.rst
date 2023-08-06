flask-oidc-ex
=============

`OpenID Connect <https://openid.net/connect/>`_ support for `Flask <http://flask.pocoo.org/>`_.

.. image:: https://img.shields.io/pypi/v/flask-oidc-ex.svg?style=flat
  :target: https://pypi.python.org/pypi/flask-oidc-ex

.. image:: https://img.shields.io/pypi/dm/flask-oidc-ex.svg?style=flat
  :target: https://pypi.python.org/pypi/flask-oidc-ex

.. image:: https://readthedocs.org/projects/flask-oidc-ex/badge/?version=latest
   :target: http://flask-oidc-ex.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/travis/larsw/flask-oidc.svg?style=flat
  :target: https://travis-ci.org/larsw/flask-oidc

This library is a fork of the `flask-oidc <https://github.com/puiterwijk/flask-oidc>` library, and should work with any standards compliant OpenID Connect provider.

The main contribution that this library provides compared to _flask_oidc_ is the option to locally validate JWT-based access tokens
(based on `python-jose <https://pypi.org/project/python-jose/>`) instead of calling the OP's userinfo endpoint for validation.

It also provides a way of providing a factory function for _httplib2.Http_ instances, so that SSL certificate validation etc. can be customized properly.

It has been tested with:

* `Keycloak <https://www.keycloak.com/>`_

Project status
==============

This project is in active development.
