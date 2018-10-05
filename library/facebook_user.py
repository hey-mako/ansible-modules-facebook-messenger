#!/usr/bin/python
"""Ansible role for managing Facebook test users.
"""
from __future__ import absolute_import

from json import dumps, loads
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = '''
---
'''

DEFAULT_CHARACTER_ENCODING = 'UTF-8'
HOST = 'graph.facebook.com'
VERSION = 'v3.1'


def main():
    module = AnsibleModule(
        argument_spec={
            'access_token': {
                'no_log': True,
                'required': True,
                'type': str
            },
            'app_id': {
                'required': True,
                'type': str
            },
            'installed': {
                'default': False,
                'type': bool
            },
            'name': {
                'default': '',
            },
            'permissions': {
                'default': [],
                'type': list
            },
            'state': {
                'choices': [
                    'absent',
                    'present'
                ],
                'default': 'present'
            },
            'test_user_id': {
                'required': False,
                'type': str
            }
        },
        supports_check_mode=True
    )
    changed = False
    access_token = module.params['access_token']
    app_id = module.params['app_id']
    state = module.params['state']
    test_user_id = module.params['test_user_id']
    method = {
        'absent': 'DELETE',
        'present': 'POST'
    }[state]
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {}
    if method == 'POST':
        path = '/{}/{}/accounts/test-users'.format(VERSION, app_id)
        data = {
            'permissions': ','.join(module.params['permissions'])
        }
    else:
        path = '/{}/{}'.format(VERSION, test_user_id)
    # Both DELETE and POST requests require access tokens.
    data['access_token'] = access_token
    # Encode the payload using the default character encoding.
    data = dumps(data).encode(DEFAULT_CHARACTER_ENCODING)
    url = 'https://{}{}'.format(HOST, path)
    request = Request(url, data=data, headers=headers, method=method)
    try:
        response = urlopen(request)
    except HTTPError as e:
        module.fail_json(msg=e.reason)
    changed = True
    json = loads(response.read())
    module.exit_json(changed=changed, status=response.status, json=json)


if __name__ == '__main__':
    main()
