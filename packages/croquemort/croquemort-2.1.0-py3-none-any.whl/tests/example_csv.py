import argparse

from nameko.standalone.rpc import ClusterRpcProxy

from croquemort.tools import generate_hash_for

config = {
    'AMQP_URI': 'amqp://guest:guest@localhost',
    'REDIS_URI': 'redis://localhost:6379/0',
}

parser = argparse.ArgumentParser()
parser.add_argument('--csvfile', type=argparse.FileType('r'), required=True)
parser.add_argument('--group')
parser.add_argument('--frequency')
args = parser.parse_args()

with ClusterRpcProxy(config) as cluster_rpc:
    for line in args.csvfile:
        url = line.strip('\n')
        cluster_rpc.http_server.fetch.async(url, args.group or None,
                                            args.frequency or None)

if args.group:
    print('Group hash: {hash}'.format(hash=generate_hash_for('group',
                                                             args.group)))
