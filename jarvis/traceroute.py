#!/usr/bin/env python
#
# This creates a graph of response times for the traceroute/ping command for monitoring
# the desired remote path
# 
from sockets import *

host = raw_input("\n"  = "IP address to trace: ")
port = 33434
ttl = 0
icmp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')
while ttl != 30:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)