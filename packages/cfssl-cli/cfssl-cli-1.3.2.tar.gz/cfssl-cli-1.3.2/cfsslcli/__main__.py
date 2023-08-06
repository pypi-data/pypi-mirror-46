#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main module
"""

from __future__ import print_function

import os

import cfssl
import click

from cfsslcli import writer, checksums, configuration
from cfsslcli.__version__ import __version__

if 'REQUESTS_CA_BUNDLE' not in os.environ:
    if os.environ.get('SSL_CERT_FILE'):
        os.environ['REQUESTS_CA_BUNDLE'] = os.environ.get('SSL_CERT_FILE')
    elif os.environ.get('NODE_EXTRA_CA_CERTS'):
        os.environ['REQUESTS_CA_BUNDLE'] = os.environ.get('NODE_EXTRA_CA_CERTS')


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(prog_name='cfssl-cli', version=__version__)
def main():
    """
    Main command group
    :return:
    """


@main.command(help='Generate certificate files')
@click.argument('domain', required=False)
@click.option('-u', '--url', help='URL of the CFSSL server')
@click.option('-n', '--common-name', help='The fully qualified domain name of the certificate')
@click.option('-h', '--host', multiple=True, help='Add hosts to the certificate')
@click.option('-c', '--config', help='Path to configuration file')
@click.option('--der', is_flag=True, help='Generates DER files')
@click.option('--csr', is_flag=True, help='Generates Certificate Request files')
@click.option('-s', '--stdout', is_flag=True, help='Display certificates on screen')
@click.option('-o', '--output', default=None, help='Write output to files of given base name')
@click.option('-d', '--destination', default=None, help='Write output files to given directory')
def gencert(url, common_name, host, config, der, csr, output, stdout, destination, domain):
    """
    Generate a new certificate.
    :param url:
    :param common_name:
    :param host:
    :param config:
    :param der:
    :param csr:
    :param output:
    :param stdout:
    :param destination:
    :param domain:
    :return:
    """
    conf = configuration.load(config, url)
    client = cfssl.CFSSL(**conf['cfssl'])

    if domain:
        common_name = domain if not common_name else common_name
        host = host + (domain, "*.%s" % domain)
        output = domain if not output else output

    if not output:
        output = common_name

    if not output:
        output = 'output'

    if not common_name:
        raise click.exceptions.ClickException("At least [domain] argument or [--common-name] option should be defined.")

    if not host:
        host = host + (common_name,)

    request = configuration.new_certificate_request(conf.get('certificate_request', {}))
    if common_name:
        request.common_name = common_name
    if host:
        request.hosts = host

    response = client.new_cert(request)

    checksums.validate_checksums(response)

    if output:
        writer.write_files(response, output, der, csr, conf.get('writer'), destination,
                           conf.get('append_ca_certificate'), client)
    if not output or stdout:
        writer.write_stdout(response, der, csr,
                            conf.get('append_ca_certificate'), client)


@main.command(help='Get CA public certificate')
@click.option('-u', '--url', help='URL of the CFSSL server')
@click.option('-c', '--config', help='Path to configuration file')
@click.option('-s', '--stdout', is_flag=True, help='Display certificates on screen')
@click.option('-o', '--output', default=None, help='Write output to files of given base name')
@click.option('-d', '--destination', default=None, help='Write output files to given directory')
def info(url, config, output, stdout, destination):
    """
    Get CA public certificate
    :param url:
    :param config:
    :param output:
    :param stdout:
    :param destination:
    :return:
    """
    conf = configuration.load(config, url)
    client = cfssl.CFSSL(**conf['cfssl'])

    response = client.info('')

    if output:
        writer.write_files(response, output, None, None, conf.get('writer'), destination,
                           False, client, False)
    if not output or stdout:
        writer.write_stdout(response, None, None,
                            False, client)


if __name__ == '__main__':
    main()
