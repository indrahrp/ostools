import getopt,sys,os,re
from pip._vendor.distlib.resources import finder
from test.test_imageop import AAAAA
#
netdevices=[]

class Devices(object):
    def __init__(self,name,ip_int,maker,dev_type,auth_type,status,version,aaa,enablepwd,localuser,staticroute,acl):
        self.name=name
        self.ip_int=ip_int
        self.maker=maker
        self.dev_type=dev_type
        self.auth_type=auth_type
        self.status=status
        self.version=version
        self.aaa=aaa
        self.enablepwd=enablepwd
        self.localuser=localuser
        self.staticroute=staticroute
        self.acl=acl
    def running_config(self):
        pass  
      
    def parse_config(self):
        pass
    
    def __str__(self):
        #return (self.name + "," + self.maker + "," + self.dev_type + "," + self.auth_type + "," +self.status+","+self.aaa+",",self.enablepwd+"," + self.localuser)
        return (self.name + "," + str(self.ip_int) +"," + self.maker + "," + self.dev_type + "," + self.auth_type + "," + \
                self.status+","+ self.version +"," + self.aaa+","+self.enablepwd+","+ self.localuser + "," +str(self.staticroute))
   
class CiscoDev(Devices):
    def parse_config(self):
        pass
    
class JuniperDev(Devices):
    def parse_config(self):
        pass


def build_device_obj(dirloc):
    try:
        print "dir loc ",dirloc
        file_list = os.listdir(dirloc)  
        print file_list
    except OSError:
        print "error"
    
    for fconfig in file_list:
        floc=dirloc + '\\' + fconfig
        print "flock " + floc
        #print dirloc.join(fconfig)
        fh=open(floc)
        #for line in fh:
        #   
        #    if  line.strip():
        #        print "file " + floc +" line  ",line.strip()
        #intlist=functoproc(fh,args);
        devicename=finddevname(fh).group()
        
        print "devi " + devicename
        version=findversion(fh)
        aaa=findaaa(fh)
        enablepwd=findenablepwd(fh)
        print "enable pwd "+enablepwd
        localuser,password=findlocaluser(fh)
        print "local user " + localuser
        
        print "version" + version
        intlist=find_int(fh)
        print "intlist " + str(intlist)
        staticroute=findstaticroute(fh)
        statroutetmp=[]
        for sta in staticroute:
            print "static ro " + sta[0]
            statroutetmp.append(sta[0])
            
        acl=findacl(fh)
        ipinspect=findipinspect(fh)
        
        netdevice=Devices(devicename,intlist,'cisco','router','radius','active',version,aaa,enablepwd,localuser,statroutetmp,acl)
        netdevices.append(netdevice)

def findstaticroute(fh):   
    fh.seek(0)
    Regex = re.compile(r'''
    #ip\s+route\s+(\d+.\d+.\d+.\d+.){0,5}
    ip\s+route\s+((\d+.\d+.\d+.\d+.)+(\w+?).*)
    ''',re.IGNORECASE | re.VERBOSE)    
    result=Regex.findall(fh.read())
    if result:
        print "staticroute is " + str(result)
        return result
    else:
        return []

def findacl(fh):
    fh.seek(0)
    print "IN FINDING ACL "
    Regex = re.compile(r'''
    access-list\s+(\d+)\s+(permit|remark|deny){1}(.*)
    #(interface\s?)(Vlan|gigabitethernet|fastethernet)(\d+/?)+\s*
    #ip\saddress\s+(\d+.\d+.\d+.\d+)\s*(\d+.\d+.\d+.\d+)?
    ''',re.IGNORECASE | re.VERBOSE)

    result=Regex.findall(fh.read())
    dictmp={}
    dictmptot={}
    listtmp=[]
    cnt = 1
    if result:
        for res in result:
            #if res[3].startswith(args[0]):
            print " acl find " + res[0] + res[1] + res[2]
            #dictmp.setdefault('type','none')
            
            dictmp['aclno']=res[0]
            dictmp['type']=res[1]
            dictmp['aclcontent']=res[2]
            listtmp.append(dictmp)
            dictmp={}
            print "lstttmp " + str(listtmp)
    
    for var in listtmp:
        dictmptot.setdefault(var['aclno'],[])
        dictmptot[var['aclno']]=dictmptot[var['aclno']] + [var]
        #print 'dictmptot ' + str(dictmptot[var['aclno']])
        print 'hasil '+  var['aclno'] + ' ' + var['type'] + ' ' + var['aclcontent']
    #dictmptot[res[0]]=listtmp
    
    for key,value in dictmptot.items():
        for val in value: 
            print 'akhir detail  dictmptot acl number '+key + 'isisny ' + val['type'] + ' ' + val['aclcontent']
    
    
def findipinspect(fh):
    fh.seek(0)
    print "IN IP INSPECT "
    
    Regex = re.compile(r'''
    ip\s+inspect\s+name\s+(\w+)(.*)
    ''',re.IGNORECASE | re.VERBOSE)

    result=Regex.findall(fh.read())
    print "Result " + str(result)
    dictmp={}
    dictmptot={}
    listtmp=[]
    if result:
        for res in result:
            #if res[3].startswith(args[0]):
            print " ip insptec find " + res[0] + res[1]
            #dictmp.setdefault('type','none')
            
            dictmp['inspect_name']=res[0]
            dictmp['content']=res[1]
            #dictmp['aclcontent']=res[2]
            listtmp.append(dictmp)
            dictmp={}
            print "lstttmp " + str(listtmp)
    
    for var in listtmp:
        dictmptot.setdefault(var['inspect_name'],[])
        dictmptot[var['inspect_name']]=dictmptot[var['inspect_name']] + [var]
        #print 'dictmptot ' + str(dictmptot[var['aclno']])
        print 'hasil '+  var['inspect_name'] + ' ' + var['content']
    #dictmptot[res[0]]=listtmp
    for key,value in dictmptot.items():
        
        #print 'akhir dictmptot acl number '+key + 'isisny ' + value['type'] + ' ' + value['aclcontent'])
        #print 'akhir dictmptot acl number '+key + 'isisny ' + str(value)
        for val in value: 
            print 'akhir detail  dictmptot inspect name '+key + ' isisny ' + val['content']

def findroutingprot():
    pass

def findallint():
    pass

def findlinevty():
    pass

def findsnmp():
    pass 

def findversion(fh):
    fh.seek(0)
    Regex = re.compile(r'''
    version\s+((\w+\W){0,3})
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)    
    result=Regex.search(fh.read())
    if result:
        print "version is " + result.group(1)
        return result.group(1)
    else:
        return 'na'

def finddevname(fh):
    fh.seek(0)
    Regex = re.compile(r'''
    hostname\s+(\w+)
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)
    result=Regex.search(fh.read())
    if result:
        return result

def findenablepwd(fh):
    fh.seek(0)
    Regex = re.compile(r'''
    enable\s+password\s+(\w+)
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)

    result=Regex.search(fh.read())
    if result:
        #print "result " + str(result.group(1))    
        return result.group(1)
    else:
        return 'na'

def findaaa(fh):
    #username jsomeone password 0 cg6#107X
    fh.seek(0)
    Regex = re.compile(r'''
    aaa\s+(\w+)
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)

    result=Regex.search(fh.read())
    if result:
        # print "result " + str(result.group(1)) 
        return result.group(0)
    else:
        return None        

def findlocaluser(fh):
    fh.seek(0)    
    Regex = re.compile(r'''
    username\s+(\w+)\s+password(.*)
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)

    result=Regex.search(fh.read())
    if result:
        #print "result " + str(result.group(2)) 
        return (result.group(1),result.group(2))
    else:
        return 'na','na' 


def find_int(fh,*args):
    fh.seek(0)
    print "in find_int args "  + str(args)
    intlist=[]
    for arg in args:
        print arg
        
    Regex = re.compile(r'''
    (interface\s?)(Vlan|gigabitethernet|fastethernet)((\d+[\.\/]?)+)\s*
    ((encapsulation\s+dot1Q\s+\d+)\s+)*
    ip\saddress\s+(\d+.\d+.\d+.\d+)\s*(\d+.\d+.\d+.\d+)?
    ''',re.IGNORECASE | re.VERBOSE|re.DOTALL)
   
    result=Regex.findall(fh.read())
    #print "result " + str(result)
    if result:
        for res in result:
            #if res[3].startswith(args[0]):
            #print "ip found " + res[0] + res[1] + res[2] + " " + res[3] + " " + res[4]
            listtmp=[res[0],res[1],res[2],res[3],res[4],res[5],res[6]]
            intlist.append(listtmp)
    return intlist




    
def findprefix(prefix):
    for device in netdevices:
        print " prefix " + prefix + " with device " + str(device.ip_int)
        #if (prefix in device.ip_int):
        for entry in device.ip_int:
            lsttmp=filter((lambda x: prefix in x) , entry)
            if lsttmp:
                for dev in lsttmp:
                    print 'with prefix ' + prefix + " sttmpyang bebnar  "+ entry[0] +' ' + entry[1] + ' ' + entry[2] +' ' + lsttmp[0] +' ' + entry[4] + ' '       
  


def findstaticrt():
    for device in  netdevices:
        if device.staticroute:
            print "device " + device.name + " wiith static route" + str(device.staticroute)
    


def usage():
    print "xxxx "


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
    
    print "in Main"
    
    #intlist=build_device_obj(r'C:\Python27\mine\network',find_prefix,"192.1.12","arg2")
    build_device_obj(r'C:\Python27\mine\network')
    for cnt in netdevices:
        print" network devices " + str(cnt)+ " ip address "
    findstaticrt()
    findprefix("192.1.")

if __name__ == "__main__":
    main()