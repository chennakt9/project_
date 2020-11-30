from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI
import sys

tree4 = TreeTopo(depth=2,fanout=2)
net = Mininet(topo=tree4)
net.start()

h1 = net.get('h1')
h2 = net.get('h2')
HOST = h1.IP()

h1.popen(f'python server.py {HOST}',stdout=sys.stdout,stderr=sys.stdout,stdin=sys.stdin)
h2.popen(f'python 1_client.py {HOST}',stdout=sys.stdout,stderr=sys.stdout,stdin=sys.stdin)

net.pingAll()
# CLI( net )

net.stop()