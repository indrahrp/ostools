#!/bin/python
import getopt,sys,os,re,ipaddress
from collections import OrderedDict 
import subprocess,re,pprint,csv
#from mine.checkhost import phys_detail


def hextodec(shex):
	netmask=[]
	#print "shex arg is " + shex
	for cnt in range(0,7,2):
		#print "cnt is " + str(cnt)
		#print 'shex is ' + shex[cnt:(cnt+2)]
		
		dec=int(shex[cnt:(cnt+2)],16)
		#print "dec is "+ str(dec)
		#netmask += "." + str(dec)
		netmask.append(str(dec))
		#print "netmask hextodec "+ netmask
	return '.'.join(netmask)

def find_int(str1):
    
    toverify=[]
    intlist=[]    
    Regex = re.compile(r'''
    (nge\d+|nxge\d+|ixgbe\d+|igb\d+|e1000g\d+).*mtu\s+(\d+).*\n\s+inet\s+(\d+.\d+.\d+.\d+)\s+netmask\s+(\w{8}).*\n\s+ether\s+(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})
    ''',re.IGNORECASE | re.VERBOSE)

    result=Regex.findall(str1)
    print "result " + str(result)
    if result:
        for res in result:
            #print "ip found " + res[0] + res[1] + res[2] + " " + res[3] + " " + res[4]
            listtmp=[]
            netmask=hextodec(res[3])
            #print "netmask is "+ netmask            
            #print "res2 is " + res[2]
            ipall= unicode(res[2]+'/'+netmask)   
       	    #important inforrmation
            #print "ipall " + ipall
            my_ip = ipaddress.ip_interface(u'100.110.120.130')
            #print "my ip " + str(my_ip)
            my_ip = ipaddress.ip_interface(ipall)
            #print "my ip " + str(my_ip) + " network " + str(my_ip.network) + " broadcast " + str(my_ip.network.broadcast_address)            
            listtmp=[res[0],res[1],res[2],res[3],res[4],netmask,str(my_ip.network),str(my_ip.network.broadcast_address)]
            intlist.append(listtmp)
            
    return intlist


def dladm_showphys(phys):
        print "dladm show-phys .."		
        active_link=subprocess.Popen(['dladm','show-phys'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines=active_link.communicate()[0]
	for line in lines.split('\n'):
		interface_up=re.compile(r'(net[0-9]+).*(up|unknown)\s+([0-9]{1,})\s+(\w+)\s+(ixgbe|igb|i40e|e1000g|nge|nxge)([0-9]+)')
                result=interface_up.findall(line) 
                for res in result:
	    		print ('result in g0 :' + res[0]+ ' g1 ' + res[1] + ' g2 ' + res[2] + ' g3 ' + res[3] + ' g4 ' + res[4] + 'g5 ' + res[5])
			phys.setdefault(res[0],{})
			phys[res[0]]['speed']=res[1]
			phys[res[0]]['duplex']=res[2]
			phys[res[0]]['device']=res[4]+res[5]
        print "phys is "+ str(phys)   
def ipadm_setip(intlist):

		prefix={'255.255.254.0':'23','255.255.255.0':'24','255.255.255.128':'25','255.255.255.192':'26','255.255.255.224':'27','255.255.255.252':'30'}
		print "ipadm setting up  .."	
        
		for int in	intlist:
			print "ipadm assign lagi to " + int[9] + " which part of " + str(int)
			print "int 2 " + int[2] + ' int 5 ' + int[5] + ' int 9 ' + int[9] + ' int 8 ' + int[8] + " key " + prefix[int[5]]
			active_link=subprocess.Popen(['ipadm','create-ip',int[9]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			lines=active_link.communicate()
			print "lines 1 error is " + lines[1]
			active_link=subprocess.Popen(['ipadm','create-addr','-T','static','-a',int[2]+'/'+prefix[int[5]],int[9]+'/'+int[8]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#print 'ipadm create-addr -T static -a' + str(int[2])+'/24'     	
			lines=active_link.communicate()
			print "lines 2 errro is " + lines[1]		
		
def ReadFromFile(Filename):
	readfile=open(Filename,'r')
	result=readfile.read()
	return result


def inttoconfigure(intl,phys):

	nintlist=[]
	for int in intl:
		print "int for looking for netname is " + str(int) +' \n'
		search_dev=int[0]
		for netname, values in phys.items():
			print "net name nad valueddevice "+ str(netname) + " : " + str(values['device'])
			if values['device'] == search_dev:
				print "netname for " +  " search_dev is " + netname			
				int.append(netname)
				nintlist.append(int)
				break
			
	#print "after all " + str(nintlist)
	return nintlist



def ping_server(serverIP,broadcast,linux):
	
    if broadcast and linux:
    	res = subprocess.call(['ping',serverIP,'-b','-s','40','-c','2'])
    elif broadcast and not linux:
    	res = subprocess.call(['ping','-s',serverIP,'50','3'])
    else:
    	res = subprocess.call(['ping',serverIP,' 3' ])
    	if res == 0:
       		print "ping to", serverIP , "OK"
   	elif res == 2:
		print "no response from", address
    	else:
        	print "ping to", serverIP, "failed!"
				
	

def pingbroadint(toverify):
	
	for ip in toverify:
		
		print "\n\n pinging brodcast ip " + ip[8] + " " + ip[7]
		ping_server(ip[7],True,False)


def gatherinfo(svrname):
	ifconfiga=ReadFromFile('/var/tmp/pkgbck/ifconfiga')
	print "ifconfiga " + ifconfiga

	#svrname=svrname
	domainname='tdn.pln.ilx.com'
	hostipdict={}

	hostfile=ReadFromFile('/var/tmp/pkgbck/hosts')
	
	print "hostfile " + hostfile
	
	for entries in hostfile.splitlines():
		hostiplist=[]
		if svrname in entries:
			#print "entry " + str(entries)
			ent=entries.split()
			hostipdict[str(ent[0])]=ent[1]
			print "\n\n"
			
	print "hostipdict "+  str(hostipdict)


	intl=find_int(ifconfiga)
	for int in intl:
<<<<<<< HEAD
		netname=str(hostipdict[int[2]]).replace('.'+ domainname,"").replace(svrname + '.' ,"")
	        print "int is " + str(int) + ' with network name ' + netname
=======
	        outname=svrname+'.'+domainname	
	        print "outname " + outname + " with hostipdict "+ str(hostipdict[int[2]]).strip()+ " with int " + int[2] 		
                if str(hostipdict[int[2]]).strip() == outname.strip():
	        	netname='out'		
	        else:
			netname=str(hostipdict[int[2]]).replace('.'+ domainname,"").replace(svrname + '.' ,"")
			#print "int is " + str(int) + ' with network name ' + netname
>>>>>>> 1505154647d377a47471ad8f310cb7c13f7fef62
		int.append(netname)
		#print "int dengan netame " + str(int)

	phys=OrderedDict()

	dladm_showphys(phys)
	print "phys is " + str(phys)


	intforconfig=inttoconfigure(intl,phys)
	#print "intforconfig is " + str(intforconfig)
	return intforconfig


#ipadm_setip(intforconfig)


#gatherinfo(svrname)
#pingbroadint(intforconfig)	

def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -A server name => to assign IP address to all server intefaces"
    print os.path.basename(sys.argv[0]) + " -B server name => to verify all interface by pinging broadcast address  "

#def validate():

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "A:B:h")
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit(0)
        if o == "-B":
            broadcastip=gatherinfo(a)
    	    pingbroadint(broadcastip)
    	if o == "-A":
            inttoconfig=gatherinfo(a)
    	    ipadm_setip(inttoconfig)
            
    
if __name__ == "__main__":
    main()
            
