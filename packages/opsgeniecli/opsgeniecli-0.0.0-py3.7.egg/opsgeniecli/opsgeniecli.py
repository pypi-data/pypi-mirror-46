#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: opsgeniecli.py
#
# Copyright 2019 Yorick Hoorneman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for opsgeniecli

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""
from datetime import timedelta
from datetime import datetime
from operator import itemgetter
import urllib.parse
import urllib.request
import os
import collections
import pathlib
import sys
import json
import requests
from prettytable import PrettyTable
import click
import pytz
# import cProfile, pstats , io

__author__ = '''Yorick Hoorneman <yhoorneman@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''26-02-2019'''
__copyright__ = '''Copyright 2019, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

#try:
#    import http.client as http_client
#except ImportError:
#    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1
#
## You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

# def profile(fnc):
#     """ A decorator that uses cProfile to profile a function """

#     def inner(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = fnc(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = SortKey.CUMULATIVE
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         print(s.getvalue())
#         return retval
#     return inner

class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = "" # pylint: disable=bad-option-value, redefined-builtin, unused-variable
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

@click.group()
@click.pass_context
@click.option('--config', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_CONFIG',
              mutually_exclusive=["team", "apikey"])
@click.option('--teamname', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAM',
              mutually_exclusive=["config"])
@click.option('--teamid', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAM',
              mutually_exclusive=["config"])
@click.option('--apikey', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_APIKEY',
              mutually_exclusive=["config"])
@click.option('--profile')
def bootstrapper(context, config, teamname, teamid, apikey, profile):
    """
Auth:

    \b
    Location of the json formatted config file:
        - Set "OPSGENIE_CONFIG" as environment variable
            example: $export OPSGENIE_CONFIG='<location>'
        - Or use --config '<location>'

    \b
    Team name & api key:
        - Set "OPSGENIE_TEAM" and "OPSGENIE_APIKEY" as environment variables
        - Or us --team and --apikey
            example: --team team5 --apikey XXXXXX

Command line examples:

    \b
    $ opsgenie teams list
    $ opsgenie teams get -id xxxxxx
    $ opsgenie teams set xxxx
    """

    if not config and not teamname and not apikey and not teamid:
        config = pathlib.PurePath(pathlib.Path.home(), ".opsgenie-cli", "config.json")
        if os.path.isfile(config):
            with open(config) as config_file:
                data = json.load(config_file)
                if not profile:
                    profile = 'default'
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
        else:
            raise click.UsageError(
                "No config was given. Do one of the following:\n"
                "\t-Create a config file at: ~/.opsgenie-cli/config.json\n"
                "\t-Specify a config file. Use --config or set the environment variable OPSGENIE_CONFIG\n"
                "\t-Specify the team & apikey. Use --team & --apikey or set the env vars OPSGENIE_TEAM & OPSGENIE_APIKEY"
            )
    elif config:
        with open(config) as config_file:
            data = json.load(config_file)
            if profile:
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
            else:
                context.obj['teamname'] = data[0]['default']['teamname']
                context.obj['apikey'] = data[0]['default']['apikey']
                context.obj['teamid'] = data[0]['default']['teamid']
    elif teamname and apikey and teamid:
        context.obj['teamname'] = teamname
        context.obj['apikey'] = apikey
        context.obj['teamid'] = teamid

@bootstrapper.group()
@click.pass_context
def alerts(context): # pylint: disable=unused-argument
    pass

@alerts.command(name='query')
@click.option('--query')
@click.pass_context
def alerts_query(context, query):
    search_query = urllib.parse.quote_plus(query)
    url = f"https://api.opsgenie.com/v2/alerts?query={search_query}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['message', 'tags', 'integration', 'createdAt'])
    for alert in parsed['data']:
        format_table.add_row([alert['message'], alert['tags'], alert['integration']['type'], alert['createdAt']])
    print(format_table)

@alerts.command(name='list')
@click.option('--active', default=False, is_flag=True)
@click.option('--moreinfo', default=False, is_flag=True)
@click.option('--limit', default=50)
@click.pass_context
def alerts_list(context, active, limit, moreinfo):
    url = f"https://api.opsgenie.com/v2/alerts?limit={limit}&query=teams:{context.obj.get('teamname')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    sortedlist = sorted(parsed['data'], key=itemgetter('status'))
    if moreinfo:
        format_table = PrettyTable(['id', 'name', 'status', 'acknowledged',
                                    'createdAt', 'tags', 'source', 'integration'])
    else:
        format_table = PrettyTable(['id', 'name', 'status', 'acknowledged', 'createdAt'])
    for item in sortedlist:
        if active:
            if item['status'] == 'open' and not item['acknowledged']: #item['acknowledged'] == False
                created_at = datetime.strptime(item['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                if moreinfo:
                    format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'],
                                          created_at, item['tags'], item['source'], item['integration']['name']])
                else:
                    format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'], created_at])
        else:
            created_at = datetime.strptime(item['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            if moreinfo:
                format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'],
                                      created_at, item['tags'], item['source'], item['integration']['name']])
            else:
                format_table.add_row([item['id'], item['message'], item['status'], item['acknowledged'], created_at])
    print(format_table)

@alerts.command(name='get')
@click.option('--id') # pylint: disable=redefined-builtin
@click.pass_context
def alerts_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/alerts/{id}"
        headers = {
            'Authorization': f"GenieKey {context.obj.get('apikey')}",
            'Content-Type': "application/json"
            }
        response = requests.request("GET", url, headers=headers)
        parsed = json.loads(response.text)
        print(json.dumps(parsed, indent=4, sort_keys=True))

@alerts.command(name='count')
@click.pass_context
def alerts_count(context):
    url = f"https://api.opsgenie.com/v2/alerts?limit=100&query=teams:{context.obj.get('teamname')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'Content-Type': "application/json"
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    dictionary = collections.Counter(item['message'] for item in parsed['data'])
    sorted_by_count = sorted(dictionary.items(), reverse=True, key=itemgetter(1))
    for alert in sorted_by_count:
        print(f"{alert[1]} - {alert[0]}")

@alerts.command(name='acknowledge')
@click.option('--id', prompt=False, cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def alerts_acknowledge(context, id, all): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/alerts/{id}/acknowledge"
        payload = '{}'
        headers = {
            'Authorization': f"GenieKey {context.obj.get('apikey')}",
            'Content-Type': "application/json"
            }
        response = requests.post(url, data=payload, headers=headers)
        parsed = json.loads(response.text)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    elif all:
        url = f"https://api.opsgenie.com/v2/alerts?query=teams:{context.obj.get('teamname')}"
        headers = {
            'Authorization': f"GenieKey {context.obj.get('apikey')}",
            'cache-control': "no-cache"
            }
        response = requests.get(url, headers=headers)
        parsed = json.loads(response.text)
        for item in parsed['data']:
            if item['status'] == 'open' and not item['acknowledged']:
                url = f"https://api.opsgenie.com/v2/alerts/{item['id']}/acknowledge"
                payload = '{}'
                headers = {
                    'Authorization': f"GenieKey {context.obj.get('apikey')}",
                    'Content-Type': "application/json"
                    }
                response = requests.request("POST", url, data=payload, headers=headers)
                if response.status_code == 202:
                    print(f"✓ - alert acknowledged: {item['id']} - {item['message']}")
                else:
                    print(f"x - alert Not acknowledged: {item['id']} - {item['message']}")

@bootstrapper.group()
@click.pass_context
def policy_alerts(context): # pylint: disable=unused-argument
    pass

@policy_alerts.command(name='list')
@click.option('--id', help='Specify the teamID for team-based alert policies instead of global policies.')
@click.pass_context
def policy_alerts_list(context, id): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/policies/alert?teamId={id}"
        print('Showing team-based alert policies only. Remove the --id to retrieve the global policies.')
    else:
        url = f"https://api.opsgenie.com/v2/policies/alert?teamId={context.obj.get('teamid')}"
        print(f"Showing team-based alert policies only for team: {context.obj.get('teamname')}")
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['id', 'name', 'enabled'])
    for item in parsed['data']:
        format_table.add_row([item['id'], item['name'], item['enabled']])
    print(format_table)

@policy_alerts.command(name='create')
@click.option('--state', type=click.Choice(['match-any-condition', 'match-all-conditions']), help='Choose if all condition should be met or atleast one.')
# @click.argument('--condition_one', nargs=4, help='field/operation/expectedValue or field/key/not(optional)/operation/expectedValue. \
#     Example: Message, contains, dynamodb. or Example2: extra-properties, host, not, regex, ^sbpojira.*$')
@click.option('--name', help='Specify the name of the alert policies.')
@click.pass_context
def policy_alerts_create(context, state, name):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/policies?teamId={context.obj.get('teamid')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        }
    body = {
        "type":"alert",
        "description":f"{name}",
        "enabled":"true",
        "filter":{
            "type":f"{state}",
            "conditions": [
                {
                    "field": "extra-properties",
                    "key": "host",
                    "not": "true",
                    "operation": "starts-with",
                    "expectedValue": "expected3"
                }
            ]
        },
        "name":f"{name}",
        "message":"{{message}}",
        "tags":["filtered"],
        "alertDescription":"{{description}}"
    }
    response = requests.post(url, headers=headers, json=body)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@policy_alerts.command(name='delete')
@click.option('--id', help='The id of the alerts policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all alerts policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def policy_alerts_delete(context, id, all): # pylint: disable=redefined-builtin, invalid-name
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
    }
    if all:
        url = f"https://api.opsgenie.com/v2/policies/alert?teamId={context.obj.get('teamid')}"
        response = requests.request("GET", url, headers=headers)
        parsed = json.loads(response.text)
        print("The following alerts policies will be deleted:")
        for item in parsed['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in parsed['data']:
                url = f"https://api.opsgenie.com/v2/policies/{item['id']}?teamId={context.obj.get('teamid')}"
                response = requests.request("DELETE", url, headers=headers)
                if response.status_code == 200:
                    print(f"alerts policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(response.text)
                    sys.exit(1)
    elif id:
        url = f"https://api.opsgenie.com/v2/policies/{id}?teamId={context.obj.get('teamid')}"
        response = requests.request("DELETE", url, headers=headers)
        if response.status_code == 200:
            print(f"alerts policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(response.text)
            sys.exit(1)
    else:
        raise click.UsageError(
            "Use --id to specify one alerts ID to remove or --all "
        )

@bootstrapper.group()
@click.pass_context
def integrations(context): # pylint: disable=unused-argument
    pass

@integrations.command(name='list')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def integrations_list(context, id, teamname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/integrations?teamId={id}"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/integrations?teamName={teamname}"
    else:
        url = f"https://api.opsgenie.com/v2/integrations"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['type', 'id', 'name', 'teamId', 'enabled'])
    for item in parsed['data']:
        format_table.add_row([item['type'], item['id'], item['name'], item['teamId'], item['enabled']])
    print(format_table)

@integrations.command(name='get')
@click.option('--id') # pylint: disable=redefined-builtin
@click.pass_context
def integrations_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/integrations/{id}"
        headers = {
            'Authorization': f"GenieKey {context.obj.get('apikey')}",
            'Content-Type': "application/json"
            }
        response = requests.get(url, headers=headers)
        parsed = json.loads(response.text)
        print(json.dumps(parsed, indent=4, sort_keys=True))

@bootstrapper.group()
@click.pass_context
def config(context): # pylint: disable=unused-argument
    pass

@config.command(name='list') # pylint: disable=undefined-variable
@click.option('--config', default="~/.opsgenie-cli/config.json", envvar='OPSGENIE_CONFIG')
def config_list(config): # pylint: disable=redefined-outer-name
    if "~" in config:
        config = os.path.expanduser(config)
    with open(config) as config_file:
        data = json.load(config_file)
        for i in data[0]:
            print(json.dumps(i, indent=4, sort_keys=True))

@bootstrapper.group()
@click.pass_context
def policy_maintenance(context): # pylint: disable=unused-argument
    pass

@policy_maintenance.command(name='get')
@click.option('--id', prompt=True)
@click.pass_context
def policy_maintenance_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v1/maintenance/{id}"
    querystring = {"teamId":f"{context.obj.get('teamid')}"}
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'Content-Type': "application/json"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@policy_maintenance.command(name='set')
@click.option('--description', prompt=True)
@click.option('--startdate', help='Example: 2019-03-15T14:34:09Z')
@click.option('--enddate', help='Example: 2019-03-15T15:34:09Z')
@click.option('--filter', help='Filter down based on the name of the notification policy.')
@click.option('--id', help='The id of the entity that maintenance will be applied.') # pylint: disable=redefined-builtin, invalid-name
@click.option('--state', type=click.Choice(['enabled', 'disabled']), default='enabled', help='State of rule that \
    will be defined in maintenance and can take \
    either enabled or disabled for policy type rules. This field has to be disabled for integration type entity rules')
@click.option('--entity', type=click.Choice(['integration', 'policy']), default='policy', help='The type of the entity \
    that maintenance will be applied. It can be either integration or policy')
@click.option('--time', type=int, help='Filter duration is hours.')
@click.pass_context
def policy_maintenance_set(context, description, id, state, entity, time, filter, startdate, enddate):  # pylint: disable=redefined-builtin, invalid-name
    if not filter and not id:
        raise click.UsageError("--id or --filter is required")
    if filter:
        url = f"https://api.opsgenie.com/v2/policies/alert?teamId={context.obj.get('teamid')}"
        headers = {
            'Authorization': f"GenieKey {context.obj.get('apikey')}",
            'Content-Type': "application/json"
            }
        response = requests.request("GET", url, headers=headers)
        parsed = json.loads(response.text)
        filtered_results = [x for x in parsed['data'] if filter in x['name']]
        if len(filtered_results) == 1:
            id = str(id[0]['id'])
        else:
            print(f"\nMultiple (alert or notification) filters found for {filter}.")
            filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
            for result in filtered_results:
                filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
            print(filtered_format_table)
            id = ""
            while len(id) < 30:
                id = click.prompt('Enter the ID of the filter you want to use', type=str)
            print(id)
    if startdate and enddate:
        start = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%SZ")
        startdatetime = start.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        enddatetime = end.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        utc_start_time = datetime.now().astimezone(pytz.utc)
        utc_end_date = utc_start_time + timedelta(hours=time)
        startdatetime = utc_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        enddatetime = utc_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.opsgenie.com/v1/maintenance"
    payload = """
        {
            "teamId": "%(named_variable_teamid)s",
            "description": "%(named_variable_description)s",
            "time": {
                "type" : "schedule",
                "startDate": "%(named_variable_startdatetime)s",
                "endDate": "%(named_variable_enddatetime)s"
            },
            "rules": [
                {
                    "state": "%(named_variable_state)s",
                    "entity": {
                        "id": "%(named_variable_id)s",
                        "type": "%(named_variable_entitytype)s"
                    }
                }
            ]
        }
""" % {'named_variable_description': description, 'named_variable_teamid': context.obj.get('teamid'),
       'named_variable_startdatetime': startdatetime, 'named_variable_enddatetime': enddatetime, 'named_variable_state': state, 'named_variable_id': id, 'named_variable_entitytype': entity}
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 201:
        if time:
            print(f"✓ - Maintenance policy created.\n\tDescription: {description}\n\tTime: {time}hours")
        if startdate and enddate:
            print(f"✓ - Maintenance policy created.\n\tDescription: {description}\n\tTime: from {startdate} - {enddate}")

@policy_maintenance.command(name='delete')
@click.option('--id', help='The id of the maintenance policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all maintenance policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def policy_maintenance_delete(context, id, all): # pylint: disable=redefined-builtin, invalid-name
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
    }
    if all:
        url = "https://api.opsgenie.com/v1/maintenance?teamId={context.obj.get('teamid')}"
        response = requests.request("GET", url, headers=headers)
        parsed = json.loads(response.text)
        print("The following maintenance policies will be deleted:")
        for item in parsed['data']:
            print(f"{item['id']} - {item['description']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in parsed['data']:
                url = f"https://api.opsgenie.com/v1/maintenance/{item['id']}"
                response = requests.request("DELETE", url, headers=headers)
                if response.status_code == 200:
                    print(f"✓ - maintenance policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(response.text)
                    sys.exit(1)
    elif id:
        url = f"https://api.opsgenie.com/v1/maintenance/{id}"
        response = requests.request("DELETE", url, headers=headers)
        if response.status_code == 200:
            print(f"✓ - maintenance policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(response.text)
            sys.exit(1)
    else:
        raise click.UsageError(
            "Use --id to specify one maintenance ID to remove or --all "
        )

@policy_maintenance.command(name='list')
@click.option('--nonexpired', '--active', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["past"])
@click.option('--past', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["non-expired"])
@click.pass_context
def policy_maintenance_list(context, nonexpired, past):
    if nonexpired:
        url = "https://api.opsgenie.com/v1/maintenance?type=non-expired"
    elif past:
        url = "https://api.opsgenie.com/v1/maintenance?type=past"
    else:
        url = "https://api.opsgenie.com/v1/maintenance"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['id', 'status', 'description', 'type', 'Startdate'])
    for item in parsed['data']:
        format_table.add_row([item['id'], item['status'], item['description'],
                              item['time']['type'], item['time']['startDate']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def heartbeat(context):  # pylint: disable=unused-argument
    pass

@heartbeat.command(name='ping')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_ping(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/heartbeats/{heartbeatname}/ping"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.post(url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@heartbeat.command(name='get')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_get(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/heartbeats/{heartbeatname}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.get(url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@heartbeat.command(name='list')
@click.pass_context
def heartbeat_list(context):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/heartbeats"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.get(url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@heartbeat.command(name='enable')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_enable(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/heartbeats/{heartbeatname}/enable"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.post(url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@heartbeat.command(name='disable')
@click.option('--heartbeatname', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_disable(context, heartbeatname):  # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/heartbeats/{heartbeatname}/disable"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.post(url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@bootstrapper.group()
def teams():
    pass

@teams.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_get(context, id, teamname):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/teams/{id}"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/teams/{teamname}?identifierType=name"
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable([parsed['data']['name'] + ' ids', parsed['data']['name'] + ' usernames'])
    for item in parsed['data']['members']:
        format_table.add_row([item['user']['id'], item['user']['username']])
    print(format_table)

@teams.command(name='logs')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_logs(context, id, teamname):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/teams/{id}"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/teams/{teamname}/logs?identifierType=name&order=desc"
    else:
        url = f"https://api.opsgenie.com/v2/teams/{context.obj.get('teamid')}"
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@teams.command(name='list')
@click.pass_context
def teams_list(context):
    url = "https://api.opsgenie.com/v2/teams"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 403:
        print(response.text)
        sys.exit(1)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['id', 'name'])
    for item in parsed['data']:
        format_table.add_row([item['id'], item['name']])
    print(format_table)

@bootstrapper.group()
def teams_routing_rules():
    pass

@teams_routing_rules.command(name='list')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def teams_routing_list(context, id, teamname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/teams/{id}/routing-rules"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/teams/{teamname}/routing-rules?teamIdentifierType=name"
    else:
        raise click.UsageError(
            "No team id or name was specified. Use --id or --teamname.\n"
        )
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@bootstrapper.group()
def escalations():
    pass

@escalations.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def escalations_get(context, id, teamname): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/escalations/{id}"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/escalations/{teamname}?identifierType=name"
    else:
        raise click.UsageError(
            "No team id or name was specified. Use --id or --teamname.\n"
        )
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@escalations.command(name='list')
@click.pass_context
def escalations_list(context):
    url = f"https://api.opsgenie.com/v2/escalations"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    format_table = PrettyTable(['id', 'name', 'ownerTeam'])
    for item in parsed['data']:
        format_table.add_row([item['id'], item['name'], item['ownerTeam']['name']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def schedules(context): # pylint: disable=unused-argument
    pass

@schedules.command(name='get')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def schedules_get(context, id, teamname):  # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/schedules/{id}"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/schedules/{teamname}?identifierType=name"
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers)
    parsed = json.loads(response.text)
    print(parsed)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@schedules.command(name='list')
@click.pass_context
def schedules_list(context):
    url = "https://api.opsgenie.com/v2/schedules"
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    parsed = json.loads(response.text)
    sortedlist = sorted(parsed['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name'])
    for item in sortedlist:
        format_table.add_row([item['id'], item['name']])
    print(format_table)

@bootstrapper.group()
@click.pass_context
def logs(context): # pylint: disable=unused-argument
    pass

@logs.command(name='download')
@click.option('--marker')
@click.option('--limit')
@click.pass_context
def logs_download(context, marker, limit):
    if limit:
        url = f"https://api.opsgenie.com/v2/logs/list/{marker}?limit={limit}"
    else:
        url = f"https://api.opsgenie.com/v2/logs/list/{marker}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'Content-Type': "application/json"
        }

    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    total_count = len(parsed['data'])
    current_count = 1
    for file in parsed['data']:
        url = f"https://api.opsgenie.com/v2/logs/download/{file['filename']}"
        print(f"{current_count} - {total_count} - downloading {file['filename']}")
        download_url = requests.request("GET", url, headers=headers)
        urllib.request.urlretrieve(download_url.text, f"/Users/yhoorneman/Downloads/{file['filename']}")
        current_count = current_count + 1

@bootstrapper.group()
@click.pass_context
def policy_notifications(context): # pylint: disable=unused-argument
    pass

@policy_notifications.command(name='get')
@click.option('--id', prompt=True)
@click.pass_context
def policy_notifications_get(context, id): # pylint: disable=redefined-builtin, invalid-name
    url = f"https://api.opsgenie.com/v2/policies/{id}"
    querystring = {"teamId":f"{context.obj.get('teamid')}"}
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))

@policy_notifications.command(name='delete')
@click.option('--id', help='The id of the notifications policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', default=False, is_flag=True, help='Will remove all notifications policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def policy_notifications_delete(context, id, all): # pylint: disable=redefined-builtin, invalid-name
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
    }
    if all:
        url = f"https://api.opsgenie.com/v2/policies/notification?teamId={context.obj.get('teamid')}"
        response = requests.request("GET", url, headers=headers)
        parsed = json.loads(response.text)
        print("The following notifications policies will be deleted:")
        for item in parsed['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in parsed['data']:
                url = f"https://api.opsgenie.com/v2/policies/{item['id']}?teamId={context.obj.get('teamid')}"
                response = requests.request("DELETE", url, headers=headers)
                if response.status_code == 200:
                    print(f"notifications policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(response.text)
                    sys.exit(1)
    elif id:
        url = f"https://api.opsgenie.com/v2/policies/{id}?teamId={context.obj.get('teamid')}"
        response = requests.request("DELETE", url, headers=headers)
        if response.status_code == 200:
            print(f"✓ - maintenance policy {id} deleted for team: {context.obj.get('teamname')}")
        else:
            print(response.text)
            sys.exit(1)
    else:
        raise click.UsageError(
            "Use --id to specify one maintenance ID to remove or --all "
        )

@policy_notifications.command(name='list')
@click.option('--id', help='Specify a teamID. The teamID from the config is used when no --id argument is given.')
@click.option('--nonexpired', '--active', default=False, is_flag=True)
@click.pass_context
def policy_notifications_list(context, id, nonexpired): # pylint: disable=redefined-builtin, invalid-name
    if id:
        url = f"https://api.opsgenie.com/v2/policies/notification?teamId={id}"
    else:
        url = f"https://api.opsgenie.com/v2/policies/notification?teamId={context.obj.get('teamid')}"
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)
    parsed = json.loads(response.text)
    sortedlist = sorted(parsed['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name', 'enabled'])
    for item in sortedlist:
        if nonexpired:
            if item['enabled']:
                format_table.add_row([item['id'], item['name'], item['enabled']])
        else:
            format_table.add_row([item['id'], item['name'], item['enabled']])
    print(format_table)

@bootstrapper.command()
@click.pass_context
def on_call(context):
    url = "https://api.opsgenie.com/v2/schedules/on-calls"
    payload = ""
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 429:
        print(response.text)
        sys.exit(1)
    else:
        parsed = response.json()
        table_eod = PrettyTable(['Team', 'EOD'])
        table_no_eod = PrettyTable(['Opsgenie teams without an EOD'])
        for item in parsed['data']:
            if item['onCallParticipants']:
                table_eod.add_row([item['_parent']['name'], item['onCallParticipants'][0]['name']])
            else:
                table_no_eod.add_row([item['_parent']['name']])
        print(table_no_eod)
        print(table_eod)

@bootstrapper.command()
@click.option('--startdate', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T14:34:09Z.')
@click.option('--enddate', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T15:34:09Z')
@click.option('--id', cls=MutuallyExclusiveOption, mutually_exclusive=["teamname"])
@click.option('--teamname', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--engineer', help='Name the username of the engineer who will be on call.')
@click.option('--hours', type=int, help='Amount of hours to set the override for.')
@click.pass_context
def override(context, id, teamname, engineer, hours, startdate, enddate): # pylint: disable=redefined-builtin, invalid-name
    """
Examples:

    \b
    $ opsgeniecli.py override --teamname <TEAMSCHEDULE> --engineer <ENGINEER> --hours <INTEGER>
    $ opsgeniecli.py override --teamname <TEAMSCHEDULE> --engineer <ENGINEER> \
        --startdate 2019-03-15T14:34:09Z --enddate 2019-03-15T15:34:09Z
    """
    if hours:
        utc_start_time = datetime.now().astimezone(pytz.utc)
        utc_end_date = utc_start_time + timedelta(hours=hours)
        startdate = utc_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        enddate = utc_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        start = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%SZ")
        startdate = start.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        enddate = end.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if id:
        url = f"https://api.opsgenie.com/v2/schedules/{id}/overrides"
    elif teamname:
        url = f"https://api.opsgenie.com/v2/schedules/{teamname}/overrides?scheduleIdentifierType=name"
    payload = """
        {
            "user" : {
                "type" : "user",
                "username": "%(named_variable_username)s"
            },
            "startDate" : "%(named_variable_start_date)s",
            "endDate" : "%(named_variable_end_date)s"
        }
    """ % {'named_variable_start_date': startdate, 'named_variable_end_date': enddate,
           'named_variable_username': engineer + "@schubergphilis.com"}
    headers = {
        'Authorization': f"GenieKey {context.obj.get('apikey')}",
        'Content-Type': "application/json"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 201:
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_time = (datetime.now() + timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"✓ - override set to {engineer} between {start_time} and {end_time}")
    else:
        print(response.text)

def main():
    """Main entry point of tool"""
    bootstrapper(obj={})  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg

if __name__ == '__main__':
    main()
