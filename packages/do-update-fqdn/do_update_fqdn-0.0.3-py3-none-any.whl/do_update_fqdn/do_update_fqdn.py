#!/bin/env python3

import json
import sys
import logging
import urllib.request
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger('do-update-fqdn')

def _get_api_response_pages(do_token, url):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {do_token}'}
    while url:
        api_request = urllib.request.Request(url, headers=headers)
        api_response = urllib.request.urlopen(api_request).read()
        jsondata = json.loads(api_response.decode('utf-8'))
        try:
            url = jsondata['links']['pages']['next']
        except KeyError:
            url = None
        yield jsondata

def get_records_by_hostname(do_token, hostname, dns_domain, rtype):
    url = f'https://api.digitalocean.com/v2/domains/{dns_domain}/records'
    for rpage in _get_api_response_pages(do_token, url):
        for do_api_record in rpage['domain_records']:
            if do_api_record['name'] == hostname and do_api_record['type'] == rtype:
                yield do_api_record


def update_record(do_token, record_id, hostname, dns_domain, rtype, data):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {do_token}'}
    # need to use double brackets to get single brackets within a formatted string
    http_body = f'{{"name": "{hostname}", "type": "{rtype}", "data": "{data}"}}'
    api_request = urllib.request.Request(f'https://api.digitalocean.com/v2/domains/{dns_domain}/records/{record_id}',
                                         headers=headers, method='PUT', data=http_body.encode('utf-8'))
    return urllib.request.urlopen(api_request).read()


def create_record(do_token, hostname, dns_domain, rtype, data):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {do_token}'}
    # need to use double brackets to get single brackets within a formatted string
    http_body = f'{{"name": "{hostname}", "type": "{rtype}", "data": "{data}"}}'
    api_request = urllib.request.Request(f'https://api.digitalocean.com/v2/domains/{dns_domain}/records',
                                         headers=headers, method='POST', data=http_body.encode('utf-8'))
    return urllib.request.urlopen(api_request).read()


parser = argparse.ArgumentParser(description='update DigitalOcean dns record')
parser.add_argument('--token', metavar='your_token', type=str, required=True, help='DO API token')
parser.add_argument('--fqdn', metavar='foo.example.com', type=str, required=True, help='fqdn that should be updated')
parser.add_argument('--type', metavar='type', type=str, required=True, help='A or AAAA or whatever')
parser.add_argument('--data', metavar='IP or other data', type=str, required=True, help='content for the record')


def cli_interface():
    exitcode = 255
    try:
        cliargs = parser.parse_args()
        hostname, dns_domain = cliargs.fqdn.split('.', maxsplit=1)
        assert (hostname), 'hostname part of fqdn seems to be empty, check your input'
        assert (dns_domain), 'domain part of fqdn seems to be empty, check your input'
        logger.info(f'set {cliargs.type} record for hostname {hostname} in domain {dns_domain} to {cliargs.data}')

        updated_records = []
        for record in get_records_by_hostname(cliargs.token, hostname, dns_domain, cliargs.type):
            logger.info('updating record with DO id %s', record['id'])
            update_record(cliargs.token, record['id'], record['name'], dns_domain, record['type'], cliargs.data)
            updated_records.append(record)
        if len(updated_records) > 1:
            logger.warning(f'warning, multiple records found for {hostname}! updated all of them')
        if len(updated_records) == 0:
            logger.info(f'no {cliargs.type} records found in {dns_domain} for hostname {hostname}, creating')
            create_record(cliargs.token, hostname, dns_domain, cliargs.type, cliargs.data)
        exitcode = 0

    except urllib.error.HTTPError as err:
        logger.info(f'DO API did not cooperate, error was {err}')
        exitcode = 2
    except:
        # if somebody knows how to do this without violating PEP8s "no bare exception clauses" gimme a call.
        # simply catching the exceptions I care about is not sufficient as the finally clause suppresses the backtrace.
        logger.exception('something went horribly wrong')
    finally:
        logging.shutdown()
        sys.exit(exitcode)


if __name__ == '__main__':
    cli_interface()
