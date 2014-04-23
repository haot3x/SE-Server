host = "yale-hout.appspot.com" 
port = "80" ##Port - 80 for http, 443 for https
#Please add all your test URLs in the followign file 
inputfile = "./url.txt"
logfile = "./url-test-log.log" ##Logfile to write actions to

import sys
import os
import os.path
import datetime
from httplib import HTTP

def wfile(detail):
	fstate = os.path.exists(logfile)
	if(fstate == 0):
		print "Logfile does not exist. Attempting to create..."
		try:
			file = open(logfile,"a+")
			file.writelines(detail)
			file.close()

		except IOError:
			print "Cannot open logfile for writing. Exiting."
			sys.exit(1)

	else:
		print "Logfile exists, writing...\n"
		file = open(logfile,"a+")
		file.writelines(detail)
		file.close()


def get(host,port,url):

	concaturl = host+url
	print "Checking Host:",concaturl
	h = HTTP(host, port)
	h.putrequest('GET', url)
	h.putheader('Host', host)
	h.putheader('User-agent', 'python-httplib')
	h.endheaders()

	(returncode, returnmsg, headers) = h.getreply()
	if returncode != 200:
		print returncode,returnmsg
		return returncode

	else:
		f = h.getfile()
		# return f.read() #returns content of page for further parsing
		print returncode, returnmsg
		return returncode


if __name__ == '__main__':
	f = open(inputfile, "r")
	for line in f:
		url = line
		now = datetime.datetime.now()
		date = now.strftime("%Y-%m-%d %H:%M:%S")
		dmsg = date+" - URL verification starting - "
		wfile(dmsg)
		concaturl = "http://"+host+url
		state = get(host,port,url)

		if(state != 200):
			msg = "Link (%s) is broken or unavailable. Return code: %s" % (concaturl,state)+"\n"
			wfile(msg)
		else:
			msg = "Link (%s) is good. Return code: %s" % (concaturl,state)+"\n"
			wfile(msg)
			print msg+"\n"