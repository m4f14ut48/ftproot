#!/usr/bin/python
"""
 * @package DDoS Attack Defender Tool for Linux
 * @version 1.0
 * @copyright (C) Copyright 2010 CMS Fruit, CMSFruit.com
 * @license GNU/GPL http://www.gnu.org/licenses/gpl-3.0.txt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
    Customize your settings below.
"""
"""
    Define the maximum number of connections allowed per IP address here.
    Fine tune this setting based on the load of your server.
    You can check the load on your system by running the following shell command:
    
    netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c

    That command will display the number of all the active TCP/IP connections to your server.
"""
MAX_CONNECTIONS_ALLOWED_PER_IP = 150 # 150 is a good/safe number for the average website

"""
    Define the email address that should receive block notifications.
    Set to empty string to disable feature.
"""
ADMIN_EMAIL = 'me@mydomain.com'

"""
    The list of IP addresses to whitelist.
    The IP Addresses in this list will NEVER be blocked.
"""
WHITELISTED_IPS = [
		    '127.0.0.1', # Prevent blocking ourself
		    '192.168.80.1', # Some IP Address on your network
		    '192.168.80.2' # Some IP Address on your network
		    ]

"""
    The duration a user should remain blocked in seconds.
    Default 600 seconds (10 minutes)
"""
BLOCK_DURATION_IN_SECONDS = 600

"""
    Define the DDoS defender log file path.
"""
DDOS_LOG_FILE = '/tmp/ddos_defender.log'

"""
    Do not modify anything below this line unless you know what you are doing!
"""

import sys
import os
import commands
import datetime

from time import sleep

class DDoSDefender:
    maximumAllowedConnectionsPerIP = 50 # maximum connections allowed per IP address
    adminEmail = '' # The email address that should receive notifications
    whitelistIPs = ['127.0.0.1']
    blockTime = 600 # The duration a user should remain blocked in seconds, Default 600 seconds (10 minutes)
    blockedIPs = {}
    keepRunning = True

    def __init__(self):
	self.setVars()

    def setVars(self):
	global MAX_CONNECTIONS_ALLOWED_PER_IP, ADMIN_EMAIL, WHITELISTED_IPS, BLOCK_DURATION_IN_SECONDS

	self.maximumAllowedConnectionsPerIP = MAX_CONNECTIONS_ALLOWED_PER_IP
	self.adminEmail = ADMIN_EMAIL
	self.whitelistIPs = WHITELISTED_IPS
	self.blockTime = BLOCK_DURATION_IN_SECONDS

    def protectSystem(self):
	self.setVars()
	
	while self.keepRunning:
	    result = commands.getoutput("netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c")
	    result = result.split("\n")

	    for line in result:
		if 'Address' in line or 'servers' in line:
		    continue
		    
		line = line.strip()
		line = line.split(' ')

		if int(line[0]) >= self.maximumAllowedConnectionsPerIP:
		    line[1] = str(line[1])
		    
		    if not line[1] in self.whitelistIPs and not self.blockedIPs.has_key(line[1]):
			os.system('/sbin/iptables -I INPUT -s '+line[1]+' -j DROP')

			now = datetime.datetime.now()
			
			self.blockedIPs[line[1]] = now+datetime.timedelta(seconds=self.blockTime)
			
			nowDisplay = str(now.strftime("%m/%d/%Y %H:%M"))

			if self.adminEmail != '':
			    os.system('echo "Banned '+line[1]+' on '+nowDisplay+' due to '+str(line[0])+' connections" | mail -s "IP addresses banned on '+nowDisplay+'" '+self.adminEmail)
			    
			sys.stdout.write(line[1]+" has been blocked because it has "+str(line[0])+" connections to this server on "+nowDisplay+".\n")
			sys.stdout.flush()

	    if len(self.blockedIPs) > 0:
		now = datetime.datetime.now()
		
		try:
		    for key in self.blockedIPs:
			if now >= self.blockedIPs[key]:
			    # Past expiration time, unblock ip
			    os.system('/sbin/iptables -D INPUT -s '+key+' -j DROP')
			    
			    nowDisplay = str(now.strftime("%m/%d/%Y %H:%M"))

			    sys.stdout.write(key+" has been unblocked on "+nowDisplay+".\n")
			    sys.stdout.flush()

			    del self.blockedIPs[key]
		except:
		    pass
		
	    sleep(0.1)

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''This forks the current process into a daemon. The stdin, stdout, and
    stderr arguments are file names that will be opened and be used to replace
    the standard file descriptors in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null. Note that stderr is
    opened unbuffered, so if it shares a file with stdout then interleaved
    output may not appear in the order that you expect. '''

    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit first parent.
    except OSError, e:
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit second parent.
    except OSError, e:
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def main ():
    """
    This is an example main function run by the daemon.
    This prints a count and timestamp once per second.
    """
    sys.stdout.write('DDoS Defender Daemon started with pid %d\n' % os.getpid() )
    sys.stdout.write('DDoS Defender Daemon stdout output\n')
    sys.stderr.write('DDoS Defender Daemon stderr output\n')

    DDoSDefender().protectSystem()

if __name__ == "__main__":
    daemonize('/dev/null', DDOS_LOG_FILE, DDOS_LOG_FILE)
    main()
