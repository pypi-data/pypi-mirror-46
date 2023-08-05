"""
    Global namespace for gmq.commands.
"""
# pylint: disable=C0103,C0325

import docopt

def build_api_opts_from_docopt_args(args):
    api_opts = {}
    _ = api_opts.update(
        {'debug': args.get('--debug')})
    _ = api_opts.update(
        {'murano_id': args.get('--uuid')})
    _ = api_opts.update(
        {'murano_token': args.get('--token')})
    _ = api_opts.update(
        {'http_timeout': args.get('--timeout'),
         'disconnect_after_seconds': args.get('--disconnect-after')})
    _ = api_opts.update(
        {'murano_host': args.get('--host')})
    _ = api_opts.update(
        {'murano_port': args.get('--port')})
    _ = api_opts.update(
        {'certfile': args.get('--cert'),
         'pkeyfile': args.get('--pkey')})
    _ = api_opts.update({'murano_cacert': args.get('--cacert')})
    _ = api_opts.update(
        {'mqtt_keepalive': args.get('--mqtt-keepalive')})
    return api_opts

