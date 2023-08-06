import requests

# Util methods used in multiple commands.


class CommandOptionsError(Exception):
    """Generic exception for insufficient args or configuration."""
    def __init__(self, *args, **kwargs):
        pass


def require_arg(args, arg_name, reason=None):
    if getattr(args, arg_name) is None:

        raise CommandOptionsError('option \'{}\' is required.{}'.format(
            arg_name.replace('_', '-'),
            f' {reason}.' if reason else ''))
    return getattr(args, arg_name)


def req_get(auth_key, url):
    headers = {}
    if auth_key:
        headers['Authorization'] = 'Bearer {}'.format(auth_key)
    return requests.get(url, headers=headers, stream=True)


def req_post(auth_key, url, data):
    headers = {'Content-Type': 'application/json'}
    if auth_key:
        headers['Authorization'] = 'Bearer {}'.format(auth_key)
    return requests.post(url, data=data, headers=headers)
