#!/bin/python
import getopt,sys,os,re,ipaddress
from collections import OrderedDict 
import subprocess,re,pprint,csv


def hextodec(shex):
	netmask=[]
	print "shex arg is " + shex
	for cnt in range(0,7,2):
		print "cnt is " + str(cnt)
		print 'shex is ' + shex[cnt:(cnt+2)]
		dec=int(shex[cnt:(cnt+2)],16)
		print "dec is "+ str(dec)
		#netmask += "." + str(dec)
		netmask.append(str(dec))
		#print "netmask hextodec "+ netmask
	return '.'.join(netmask)

def find_int(str1):
    
    intlist=[]    
    Regex = re.compile(r'''
    (ixgbe\d+|igb\d+|e1000g\d+).*mtu\s+(\d+).*\n\s+inet\s+(\d+.\d+.\d+.\d+)\s+netmask\s+(\w{8}).*\n\s+ether\s+(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})
    ''',re.IGNORECASE | re.VERBOSE)

    #print "sting ins" + str1
    result=Regex.findall(str1)
    print "result " + str(result)
    if result:
        for res in result:
        	#listtmp=[]
            ###if res[3].startswith(args[0]):
            print "ip found " + res[0] + res[1] + res[2] + " " + res[3] + " " + res[4]
            listtmp=[]
            netmask=hextodec(res[3])
            print "netmask is "+ netmask            
            print "res2 is " + res[2]
            #ipall='u' + "'"+ res[2]+'/'+netmask + "'"
            ipall= unicode(res[2]+'/'+netmask)
            
            print "ipall " + ipall
            my_ip = ipaddress.ip_interface(u'100.110.120.130')
            print "my ip " + str(my_ip)
            my_ip = ipaddress.ip_interface(ipall)
            print "my ip " + str(my_ip) + " network " + str(my_ip.network) + " broadcast " + str(my_ip.network.broadcast_address)            
            listtmp=[res[0],res[1],res[2],res[3],res[4],netmask]
            intlist.append(listtmp)
            #print "listtmp " + str(listtmp)
    return intlist


def dladm_showphys(phys):
        print "dladm show-phys .."		
        active_link=subprocess.Popen(['dladm','show-phys'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines=active_link.communicate()[0]
	for line in lines.split('\n'):
		interface_up=re.compile(r'(net[0-9]+).*up\s+([0-9]{1,})\s+(\w+)\s+(ixgbe|igb|i40e|e1000g)([0-9]+)')
                result=interface_up.findall(line) 
                for res in result:
	    		print ('result in g0 :' + res[0]+ ' g1 ' + res[1] + ' g2 ' + res[2] + ' g3 ' + res[3] + ' g4 ' + res[4] )
			phys.setdefault(res[0],{})
			phys[res[0]]['speed']=res[1]
			phys[res[0]]['duplex']=res[2]
			phys[res[0]]['device']=res[3]+res[4]

def ipadm_setip(intlist):

		prefix={'255.255.254.0':'23','255.255.255.0':'24','255.255.255.128':'25','255.255.255.192':'26','255.255.255.224':'27'}
		print "ipadm setting up  .."	
        
		for int in	intlist:
			#print "ipadm assign to pertama " + int[7]
			print "ipadm assign lagi to " + int[7]
			active_link=subprocess.Popen(['ipadm','create-ip',int[7]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			lines=active_link.communicate()
			print "lines 1 error is " + lines[1]
			active_link=subprocess.Popen(['ipadm','create-addr','-T','static','-a',int[2]+'/'+prefix[int[5]],int[7]+'/'+int[6]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print 'ipadm create-addr -T static -a' + str(int[2])+'/24'     	
			lines=active_link.communicate()
			print "lines 2 errro is " + lines[1]		
		
def ReadSwitchConfigFromFile(Filename):
	readfile=open(Filename,'r')
	result=readfile.read()
	return result

ifconfiga=ReadSwitchConfigFromFile('ifconfiga')
print "ifconfiga " + ifconfiga

svrname='bunkerx1'
domainname='tdn.pln.ilx.com'
hostipdict={}

hostfile=ReadSwitchConfigFromFile('hosts')
#print "hostfile is : " + hostfile
for entries in hostfile.splitlines():
	#print "entry1 " + entry
	hostiplist=[]
	if svrname in entries:
		print "entry " + str(entries)
		ent=entries.split()
		#hostiplist=[ent[1]]		
		hostipdict[str(ent[0])]=ent[1]
		print "\n\n"
			
print "hostipdict "+  str(hostipdict)

intl=find_int(ifconfiga)
for int in intl:
	netname=str(hostipdict[int[2]]).replace('.'+ domainname,"").replace(svrname + '.' ,"")
	#print "int is " + str(int) + ' with network name ' + netname
	int.append(netname)
	print "int dengan netame " + str(int)

phys=OrderedDict()

dladm_showphys(phys)
print "phys is " + str(phys)



def inttoconfigure():

	nintlist=[]
	for int in intl:
		print "int for looking for netname is " + str(int) +' \n'
		search_dev=int[0]
		for netname, values in phys.items():
			if values['device'] == search_dev:
				print "netname for " +  " search_dev is " + netname
			
				int.append(netname)
				nintlist.append(int)
				break
				#print values['device']
	print "after all " + str(nintlist)
	return nintlist

intforconfig=inttoconfigure()
print "intforconfig is " + str(intforconfig)
ipadm_setip(intforconfig)

def usage():
    print "xxxx "

#def validate():



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq")
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit(0)
        if o == "-q":
            print "test"
    
if __name__ == "__main__":
    main()
            