import getopt,sys,os,re
from collections import OrderedDict 
import subprocess,re,pprint,csv
#from pip._vendor.distlib.resources import finder
#from test.test_imageop import AAAAA
#str1="ixgbe5: flags=1001000843<UP,BROADCAST,RUNNING,MULTICAST,IPv4,FIXEDMTU> mtu 9000 index 10\
#	inet 10.110.16.101 netmask ffffff00 broadcast 10.110.16.255\
#	ether 90:e2:ba:3e:d2:fd"

#str1="ixgbe5: flags=1001000843<UP,BROADCAST,RUNNING,MULTICAST,IPv4,FIXEDMTU> mtu 9000 index 10"
#print str1 


def find_int(str1):
    
    intlist=[]    
    #Regex = re.compile(r'''
    #(ixgbe\d+).*inet\s*(\d+.\d+.\d+.\d+)\+s*netmask\s*(\w\w.\w\w.\w\w.\w\w).*
    #''',re.IGNORECASE | re.VERBOSE|re.DOTALL)
    #(ixgbe|igb|lo)(\d+).*mtu\s+(\d+).*\n\s+inet\s+(\d+.\d+.\d+.\d+)\s+netmask\s+(\w{7}).*\n\s+ether\s+(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)
    #''',re.IGNORECASE | re.VERBOSE)
    Regex = re.compile(r'''
    (ixgbe\d+|igb\d+).*mtu\s+(\d+).*\n\s+inet\s+(\d+.\d+.\d+.\d+)\s+netmask\s+(\w{7}).*\n\s+ether\s+(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})
    ''',re.IGNORECASE | re.VERBOSE)

    
    #print "sting ins" + str1
    result=Regex.findall(str1)
    print "result " + str(result)
    if result:
        for res in result:
        	#listtmp=[]
            ###if res[3].startswith(args[0]):
            ###print "ip found " + res[0] + res[1] + res[2] + " " + res[3] + " " + res[4]
            listtmp=[]
            listtmp=[res[0],res[1],res[2],res[3],res[4]]
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
        print "ipadm setting up  .."	
        for int in	intlist:
        
        	active_link=subprocess.Popen(['ipadm','-T','static','-a','show-phys'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        	lines=active_link.communicate()[0]
			
		
def ReadSwitchConfigFromFile(Filename):
	readfile=open(Filename,'r')
	result=readfile.read()
	return result

ifconfiga=ReadSwitchConfigFromFile('ifconfiga')
print "ifconfiga " + ifconfiga

intl=find_int(ifconfiga)
for int in intl:
	print "int is " + str(int) +' \n'


    
#fh=open(r'C:\Python27\mine\network\showrun2800router.txt')

#egex = re.compile(r'''
#   interface\s?(Vlan|gigabitethernet|fastethernet)(\d+/?)+\s*
#    ip address (\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+)
#p\saddress\s+(\d+.\d+.\d+.\d+)\s*(\d+.\d+.\d+.\d+)?
#'',re.IGNORECASE | re.VERBOSE|re.DOTALL)
Regex = re.compile(r'''
    (interface\s?)(Vlan|gigabitethernet|fastethernet)(\d+/?)+\s*
    ip\saddress\s+(\d+.\d+.\d+.\d+)\s*(\d+.\d+.\d+.\d+)?
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)

#result=Regex.findall(fh.read())

#if result:
#	for res in result:
#           #if res[3].startswith(args[0]):
#            print "ipsfound " + res[0] + res[1]+str(res[2])


phys=OrderedDict()
physL=OrderedDict()
result=OrderedDict()
intfresult=OrderedDict()
z2_detail=OrderedDict()
dladm_showphys(phys)
print "phys is " + str(phys)
search_dev='e1000g0'
for int in intl:
	print "int is " + str(int) +' \n'
	search_dev=int[0]
	for netname, values in phys.items():
		if values['device'] == search_dev:
			print "netname for " +  " search_dev is " + netname
			intl
			int[5]=netname
			break
			#print values['device']
print "after all " + str(intl)
#dladm_showphys_L(phys,physL)

##print "phys"
##print  phys
##print "physL"
##print  physL

#find_slot_info(phys,physL,result)
            