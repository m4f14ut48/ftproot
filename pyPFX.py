#!/usr/bin/env ptyhon
# Author - ecophobia@gmail.com
'''
 This code uses chilkat libraries to locate password of PFX Certificate. It does not decrypt the message Upon successfull match of a wordlist
 the code writes located password into 'password.txt' file and exits.
'''
import sys
import chilkat
import string
import Tkinter, tkFileDialog


wordlistFormats = [
    ('Text file','*.txt'),
    ('Dictionary file','*.dic'),
    ('List file','*.lst')]
certificateFormat = [('Personal Information Exchange', '*.pfx')]
encmessageFormat = [('PKCS 7 MIME Message', '*.p7m')]

root = Tkinter.Tk()
root.withdraw()
wordlist = tkFileDialog.askopenfilename(parent=root,filetypes=wordlistFormats,title='Choose [txt; dic; lst] wordlist')
certificate = tkFileDialog.askopenfilename(parent=root,filetypes=certificateFormat,title='Choose PFX Certificate')
encmessage = tkFileDialog.askopenfilename(parent=root,filetypes=encmessageFormat,title='Choose PKCS 7 MIME [p7m] Message')

def counter(): # Wordlist counter
    counter = 0
    with open(wordlist, 'r') as textf:
        for line in textf:
            counter += 1
        return counter
    
print "Please wait! Checking the wordlist."
# -----------------------------------------------------------
total = counter() 
print '\n\nThere are ', format(total,',d'), ' words in the wordlist.'
raw_input('\nPress any key to continue!\n') 

#--------Start Tracking Time-----
import datetime
startTime = datetime.datetime.now()
#-----------------

crypt = chilkat.CkCrypt2()

success = crypt.UnlockComponent("Anyting for 30-day trial") # Use chilkat crypt code instead of "Anyting for 30-day trial" to unlock. It is Licensed and commercial
if (success != True):
    print crypt.lastErrorText()
    sys.exit()
#  Read the P7M file into memory.
p7mData = chilkat.CkByteData()
success = crypt.ReadFile(str(encmessage),p7mData)
if (success != True):
    print crypt.lastErrorText()
    sys.exit()
#  Setup the crypt object: Indicate that public-key decryption is to be used.
crypt.put_CryptAlgorithm("pki")

#  Add a PFX file to allow the crypt object to find
#  the certificate and private key needed for decryption
pfxFilePath = str(certificate)

pfxPassword = 'whatever' # Activating pfxPassword with dummy password

progressMon = 0
with open(str(wordlist), 'r') as mywordlist:
    for pfxPassword in mywordlist:
        progressMon += 1
        sys.stdout.write ("\r%.2f%%" % (100 * float(progressMon)/float(total)))
        sys.stdout.flush()
        success = crypt.AddPfxSourceFile(pfxFilePath,pfxPassword.strip())
        if (success == True):
            password = open('password.txt','w')
            password.write(pfxPassword.strip())
            password.close()
            print '\nSuccess!!! :-)\nLocated Password is: ', pfxPassword
            #---- Finish Timing ------------
            finishTime = datetime.datetime.now() - startTime
            print "The program finished in :", finishTime
            #-----------------------------
            raw_input('Type any key to exit')
            sys.exit()
#---- Finish Timing ------------
finishTime = datetime.datetime.now() - startTime
print "\n\nUnable to locate password :-(\n\nThe program finished in :::", finishTime
#-----------------------------
raw_input('\nPress any key to exit')