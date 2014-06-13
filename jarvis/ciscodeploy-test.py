#!usr/bin/env python
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
# 09-26-13 - v 0.2 Alpha

import sys
import time
import getpass
import select
import os
import paramiko

# Get current path
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

# Gather functional requirements from the user
user = 'mtcadmin'
pass1 = 'JU$#@ws234!!!!'
host = '99.170.3.101'
port = 2009
# Files that have host list and configs to push
devicefile = dir_path + '/hosts.txt'
commandfile = dir_path + '/config.txt'
# Opens files in read mode
f1 = open(devicefile, "r")
f2 = open(commandfile, "r")
# Create list based on files above
devices = f1.readlines()
commands = f2.readlines()
i = 1
# To copy from the config.txt file for pushing across the wire

# Starts the deploy
# Open this as read-only or open a text box to paste in configs
while True:
	print "Trying to connect to %s (%i/30)" % (host, i)
	try:
		ssh = paramiko.SSHClient()
# Add fingerprint or remote device
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Passes variables from above
		#ssh.connect(host, port, user, pass1)
		print "Connected to %s" % host
		break
	except paramiko.AuthenticationException:
		print "Authentication failed when connecting to %s" % host
		i += 1
		time.sleep(1)
		# If we could not connect within time limit
	if i == 3:
		print "Could not connect to %s. Giving up" % host
		sys.exit(1)
# Copying running-config to local machine
cmd = 'y'
print ("\n" + "Type q to quit")
#while True:
def connect_to(x):
	for device in x:
		#cmd = raw_input("\n" + "Command to pass: ")
		for command in commands:
			command = command.rstrip()
			ssh.connect(host, port, user, pass1)
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
			output = open(device + ".out", "a")
			output.write("\n\nCommand Issued: " +command+"\n")
			output.writelines(ssh_stdout)
			output.write("\n")
			print 'You are done'
	# Flushes buffer to terminal
	#ssh_stdin.flush()
	#for line in ssh_stdout.readlines():
	#	print line
	for line in ssh_stderr.readlines():
		print line
	#while True:
	#	if ssh_stdout.channel.exit_status_ready():
	#		break
	#	rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
	#	if len(rl) > 0:
	#		print ssh_stdout.channel.recv(9999999)
	if cmd == 'q':
	# Disconnect from the host
		print "Command done, closing SSH connection"
		print '\a'
		ssh.close()
		#break