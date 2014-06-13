#!/usr/bin/env python
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

import os
import sys

# Cycles through menu selections
while quit != 'q':
# Menu options for different commands
	print "\n" + 'Welcome to ITS!'
	print "\n" + '------------------------------------'
	print '1. IP Calculator                    |'
	print '2. Deploy Cisco Configs             |'
	print '3. DDos                             |'
	print '4. Scan ports of an IP address      |'
	print '5. Readme.txt                       |'
	print 'q = Quit                            |'
	print '------------------------------------'
	
# Input for selection
	y = raw_input("\n" + "Please make a selection: ")
# Starts the process selected
	if y == 'q':
		break
	elif y == '1':
		import subnetcalc
	elif y == '2':
		import ciscodeploy
	elif y == '3':
		import ddos
	elif y == '4':
		import portscan
	elif y == '5':
		print 'Readme.txt information goes here, linking to the file'
		quit = raw_input("Press ENTER to try again or q to quit:  ")
	else:
		# Incorrect input
		print 'Please enter a valid selection. Use the number next to desired command'
		quit = raw_input("Press ENTER to try again or q to quit:  ")