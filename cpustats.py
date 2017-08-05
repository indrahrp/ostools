import re
import datetime



#fd=open('C:\temp\wrk.txt')

#fd=open("c:\\temp\\testfile",'r')
fd=open("C:\Users\uc205955\Downloads\sysinfo.fri",'r')
#    print line
#for line in fd:
#    print line
#str1=fd.read()   
#print str
#print str1

def find_cpu(fd):
    for line in fd:
        intlist=[]    
        #print line
        Regex = re.compile(r'''
        (\d+)\s+(\d{1,2})\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+ 
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)
    #print str2
    #print "result " + str(result)
        if result:
            if float(result.group(11)) < 30 :
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                #print result.group(2,11)
                #print result.group(2)
                print  ctime + "  " + result.group(2) + " " + result.group(11)
            #print "ip found " + res[0] + res[1] + res[2] + " " + res[3] + " " + res[4]
            #    listtmp=[]
          
            #   intlist.append(listtmp)
            
                #return intlist

find_cpu(fd)

# Regex = re.compile(r'''
#        <Hyper-threading>(\w+)</Hyper-threading>
#        ''',re.IGNORECASE | re.VERBOSE )