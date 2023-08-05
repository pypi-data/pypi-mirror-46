.. image:: http://img.shields.io/pypi/v/cfssl-cli.svg
  :target: https://pypi.python.org/pypi/cfssl-cli
  :alt: Latest Version

.. image:: http://img.shields.io/badge/license-MIT-blue.svg
  :target: https://pypi.python.org/pypi/cfssl-cli
  :alt: MIT License

.. image:: http://img.shields.io/travis/Toilal/python-cfssl-cli.svg
  :target: https://travis-ci.org/Toilal/python-cfssl-cli
  :alt: Build Status

Python CFSSL CLI
================

This CLI tool allows you to generate certificates from a remote CFSSL server.

CFSSL is CloudFlare's open source toolkit for everything TLS/SSL. CFSSL is used by
CloudFlare for their internal Certificate Authority infrastructure and for all of
their TLS certificates.

* `Read more on the CloudFlare blog
  <https://blog.cloudflare.com/introducing-cfssl/>`_.
* `View the CFSSL source
  <https://github.com/cloudflare/cfssl>`_.

Requirements
============

A pre-existing CFSSL server is required to use this library.

Installation
============

* Install Python package ``pip install cfssl-cli``