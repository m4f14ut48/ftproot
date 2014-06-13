#!/usr/bin/ env python
#
from random import randint

play = 'y'
print "To exit the game early, press the CTRL + C, then CTRL + Z, and press ENTER"
while play != 'n':
	a = int('2')
	b = randint(1, 10)
	c = a + b
	print '\n'
	print a,  '+',  b
	print 'What\'s the sum?'
	d = int(raw_input())
	while d != c:
		print 'Wrong, try again!'
		d = int(raw_input())
	else:
		print "Correct!"
	play = raw_input("Do you want to play again? y/n: ")
	if play == 'n':
		print "Thanks for playing, Tatum!"
		break