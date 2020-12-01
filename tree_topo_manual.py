from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
import os

from time import sleep


PORT = 12345



## Custom Topo 2

class CustomTopo2(Topo):
	def build(self, bw):
		h1 = self.addHost("h1")
		h2= self.addHost("h2")
		h3 = self.addHost("h3")
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')
		s6 = self.addSwitch('s6')
		s7 = self.addSwitch('s7')
		h4= self.addHost("h4")
		h5= self.addHost("h5")
		h6 = self.addHost("h6")
		h7 = self.addHost("h7")
		h8= self.addHost("h8")
		h9= self.addHost("h9")
		h10= self.addHost("h10")
		h11= self.addHost("h11")
		self.addLink(h4 ,s4, bw=bw)       
		self.addLink(h5 ,s4, bw=bw)  
		self.addLink(h6, s5, bw=bw)
		self.addLink(h7, s5, bw=bw)
		self.addLink(h8, s6, bw=bw)
		self.addLink(h9, s6, bw=bw)
		self.addLink(h10, s7, bw=bw)
		self.addLink(h11, s7, bw=bw)
		self.addLink(s4, s2, bw=bw*2)
		self.addLink(s5, s2, bw=bw*2)
		self.addLink(s6, s3, bw=bw*2)
		self.addLink(s7, s3, bw=bw*2)
		self.addLink(s2, s1, bw=bw*4)
		self.addLink(s3, s1, bw=bw*4)
		self.addLink(s1, h1, bw=bw*4)
		self.addLink(s6, h2, bw=bw)
		self.addLink(s7, h3, bw=bw)




net = Mininet(CustomTopo2(bw=10), link=TCLink,cleanup=True)
net.start()
# net.pingAll()
CLI(net)



net.stop()



