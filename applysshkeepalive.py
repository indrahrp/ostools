#!/usr/bin/python

import subprocess,re,pprint,csv
from collections import OrderedDict


root='/home/i/indrah/collect2/'
sshkeepalive=root + 'configsys6'
serverlist=[]

def find_server(serverlist):
        print "\n\nFinding Server Info from Master Sheet\n\n "
        with open('z1logical') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                        #print "row 0 "+ row[0] + " hostname " + hostname
                        	serverlist.append(row[0])
			        #print row[0]   	

def apply_changes(hostname):
	#hostname='tigerz2'
	#print sshkeepalive
	print "updating server sshd_config " + hostname
	active_link=subprocess.Popen([sshkeepalive,'-K',hostname], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err=active_link.communicate()
	for line in out.split('\n'):
		print line
	for line in err.split('\n'):
		print line


find_server(serverlist)
serverlist_uniq = set (serverlist)

start=81
end=90
cnt=0
for server in serverlist_uniq:
        cnt=cnt + 1  
	#print "server is "+ server
	if cnt >= start and cnt <= end:  
		print "applying clientalive on " + server
		apply_changes(server)
	
