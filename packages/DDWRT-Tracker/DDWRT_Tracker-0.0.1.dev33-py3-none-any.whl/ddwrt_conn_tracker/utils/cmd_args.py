import argparse

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('--host', help='router SSH host', dest='host')
parser.add_argument('-H', help='router SSH host', dest='host')
parser.add_argument('--port', help='router SSH port (normally 22)')
parser.add_argument('-p', dest='port')
parser.add_argument('--user', help='router SSH user')
parser.add_argument('-u', dest='user')
parser.add_argument('--pwd', help='router SSH password')
parser.add_argument('-P', dest='pwd')
parser.add_argument('--mode')

args = parser.parse_args()

start_args = {}
if args.host and args.mode != 'client':
    start_args = dict(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.pwd
            )
