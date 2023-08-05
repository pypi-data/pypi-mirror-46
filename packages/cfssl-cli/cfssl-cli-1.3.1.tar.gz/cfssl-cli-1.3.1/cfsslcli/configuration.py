#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration module
"""

import os
from os.path import expanduser, expandvars, normpath, join, dirname, exists
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

import cfssl
import pkg_resources
import yaml

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin


def load(configuration, url=None):
    """
    Load the configuration

    :param configuration:
    :return:
    """
    configuration = find_configuration(configuration)
    if configuration and not exists(configuration):
        write_default_configuration(configuration)

    if configuration and exists(configuration):
        with open(configuration, 'r') as stream:
            loaded = yaml.load(stream, Loader=yaml.FullLoader)
            loaded['__configuration__'] = configuration
            if 'writer' in loaded:
                loaded['writer']['__configuration__'] = configuration
            if url is None:
                url = os.environ.get('CFSSL_URL')
            if url:
                parsed = urlsplit(url)
                loaded['cfssl']['ssl'] = parsed.scheme.lower() == 'https'
                loaded['cfssl']['verify_cert'] = parsed.scheme.lower() == 'https'
                loaded['cfssl']['host'] = parsed.hostname
                try:
                    loaded['cfssl']['port'] = parsed.port
                except ValueError:
                    pass
            if os.environ.get('CFSSL_VERIFY_CERT'):
                loaded['cfssl']['verify_cert'] = True
            if os.environ.get('CFSSL_NO_VERIFY_CERT'):
                loaded['cfssl']['verify_cert'] = False
            return loaded
    else:
        raise FileNotFoundError('Can\'t find configuration file: %s' % configuration)


def find_configuration(configuration):
    """
    Find the configuration filepath.

    :param configuration:
    :return:
    """
    if configuration:
        configuration = normpath(expandvars(expanduser(configuration)))
        return configuration

    home = os.environ.get('CFSSL_CLI_HOME', join('~', '.cfssl-cli'))
    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser('cfssl-cli.yml')))

    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser(join('.cfssl-cli', 'config.yml'))))

    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser(join(home, 'config.yml'))))

    return configuration


def write_default_configuration(configuration):
    """
    Write default configuration file.
    :param configuration:
    :return:
    """
    default_config_content = pkg_resources.resource_string(__name__, 'config/config.yml')
    dirs = dirname(configuration)
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)
    with open(configuration, 'wb') as stream:
        stream.write(default_config_content)


def _load_configuration_property(certificate_request, configuration, key, value):
    if not value:
        try:
            value = configuration[key]
        except KeyError:
            pass

    if value:
        setattr(certificate_request, key, value)


def new_certificate_request(configuration, common_name=None, hosts=None):
    """
    Creates a CertificateRequest based on configuration

    :param configuration:
    :param common_name:
    :return:
    """
    certificate_request = cfssl.CertificateRequest()

    _load_configuration_property(certificate_request, configuration, 'common_name', common_name)
    _load_configuration_property(certificate_request, configuration, 'hosts', hosts)

    return certificate_request
