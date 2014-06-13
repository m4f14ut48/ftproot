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
user = raw_input("Please enter your username: ")
pass1 = getpass.getpass("Please enter your password: ")
host = raw_input("Please put in IP address: ") # Add ability to browse for hosts.txt file of IP addresses
port = int(raw_input("What port does the remote device use for SSH? "))
file = raw_input("Please give the file name for your configurations: ")
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
		ssh.connect(host, port = port, username=user, password=pass1)
		print "Connected to %s" % host
		break
	except paramiko.AuthenticationException:
		print "Authentication failed when connecting to %s" % host
		i += 1
		time.sleep(2)

		# If we could not connect within time limit
	if i == 30:
		print "Could not connect to %s. Giving up" % host
		sys.exit(1)
		
# Pass commands, example is 'ls'
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
print("\nstdout is:\n" + ssh_stdout.read() + "\nstderr is:\n" + ssh_stderr.read())
# To copy files to the remote machine; should move to it's own module to call
sftp = ssh.open_sftp()
# sftp.get('flash:/config.txt', dir_path + '/retrieved.txt')
sftp.put(dir_path + '/' + file, '/home/pi/Desktop/mathcards.py')
# Flushes inputs
ssh_stdin.flush()
# Validate config syntax, ensure the command is issued correctly. This will be a huge 
# undertaking... :-/ Also need to know if a command failed
# Wait for the command to terminate
while True:
	if ssh_stdout.channel.exit_status_ready():
		break
	rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
	if len(rl) > 0:
		print ssh_stdout.channel.recv(1024)

# Disconnect from the host
print "Command done, closing SSH connection"
print '\a'
ssh.close()