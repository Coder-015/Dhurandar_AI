#!/usr/bin/env python3
"""
Mininet Topology Script for DhurandarAI

Simulates a small network topology with:
- 1 Router (r1)
- 1 Firewall (fw1 - simulated as a switch between router and internal network)
- 1 Server (s1)
- 3 Client machines (h1, h2, h3)
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    """Network topology for DhurandarAI."""
    def build(self):
        # Add Router
        router = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        
        # Add Firewall (using a switch as a basic representation of a firewall/choke point)
        firewall = self.addSwitch('fw1')
        
        # Add internal switch connecting clients and server
        sw1 = self.addSwitch('sw1')
        
        # Add Server
        server = self.addHost('s1', ip='10.0.0.100/24', defaultRoute='via 10.0.0.1')
        
        # Add Clients
        h1 = self.addHost('h1', ip='10.0.0.11/24', defaultRoute='via 10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.12/24', defaultRoute='via 10.0.0.1')
        h3 = self.addHost('h3', ip='10.0.0.13/24', defaultRoute='via 10.0.0.1')
        
        # Create links
        # Router <-> Firewall
        self.addLink(router, firewall, intfName1='r1-eth0', intfName2='fw1-eth1')
        
        # Firewall <-> Internal Switch
        self.addLink(firewall, sw1)
        
        # Connect hosts and server to internal switch
        self.addLink(h1, sw1)
        self.addLink(h2, sw1)
        self.addLink(h3, sw1)
        self.addLink(server, sw1)

def run():
    topo = NetworkTopo()
    # Note: Using default controller and OVS switch
    net = Mininet(topo=topo, controller=Controller, switch=OVSKernelSwitch)
    net.start()
    
    info("*** Routing Table on Router:\n")
    info(net['r1'].cmd('route'))
    
    info("*** Running CLI\n")
    CLI(net)
    
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
