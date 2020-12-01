from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI







class CustomTopo(Topo):
	def build(self):
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')
		s6 = self.addSwitch('s6')
		s7 = self.addSwitch('s7')

		h1 = self.addHost("h1")
		h2 = self.addHost("h2")
		h3 = self.addHost("h3")
		h4 = self.addHost("h4")
		h5 = self.addHost("h5")
		h6 = self.addHost("h6")
		h7 = self.addHost("h7")
		h8 = self.addHost("h8")
		h9 = self.addHost("h9")
		h10= self.addHost("h10")
		h11= self.addHost("h11")

		self.addLink(h4 ,s4)       
		self.addLink(h5 ,s4)  
		self.addLink(h6, s5)
		self.addLink(h7, s5)
		self.addLink(h8, s6)
		self.addLink(h9, s6)
		self.addLink(h10, s7)
		self.addLink(h11, s7)
		self.addLink(s4, s2)
		self.addLink(s5, s2)
		self.addLink(s6, s3)
		self.addLink(s7, s3)
		self.addLink(s2, s1)
		self.addLink(s3, s1)
		self.addLink(s1, h1)
		self.addLink(s6, h2)
		self.addLink(s7, h3)




net = Mininet(CustomTopo, link=TCLink,cleanup=True)
net.start()
# net.pingAll()
CLI(net)



net.stop()



