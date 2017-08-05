import re
import datetime,getopt
from time import ctime



#fd=open('C:\temp\wrk.txt')

#fd=open("c:\\temp\\testfile",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.fri",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.thu",'r')
fd=open("C:\\temp\\sysinfo1.wed")


#    print line
#for line in fd:
#    print line
#str1=fd.read()   
#print str
#print str1

def find_cpu(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    i=0
    for line in fd:
        intlist=[]    
        #print line
        Regex = re.compile(r'''
        (\d+)\s+(\d{1,2})\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+ 
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)
    #print str2
    #print "result " + str(result)
        if result:
            if float(result.group(23)) <= 90:
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                #print result.group(2,11)
                #print result.group(2)
                print  ctime + "  " + result.group(2) + " " + result.group(23)
                print result.group(0)
                i=i+1
                if i==100:
                    raw_input('enter')
                
            #   intlist.append(listtmp)
            
                #return intlist

def find_nicstat(fd):
    i=0
    for line in fd:
        #print line
        Regex = re.compile(r'''
        (\d+)\s+(\d+):(\w+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+)\:(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):
        (\+\.\d+):(\d+\.\d+) 
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)        
        
        if result:
            #print "resut "+result.group(0)
            #if float(result.group(5)) > 5300 and result.group(3).strip() == 'p3p1':
            #if result.group(3).strip() == 'p3p1':
            
            if float(result.group(4)) > 0:
            
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                #print result.group(2,11)
                #print result.group(2)
                #print  ctime + "  " + result.group(2) + " " + result.group(8) 
                print  ctime + "  " + result.group(3) + "    " + result.group(4)  + \
                "   " + result.group(5)
                #print  ctime + "  " + result.group(0) 
                i=i+1
                if i==30:
                    i=0
                    raw_input('enter')
                


def find_iostat(fd):
    #r/s,w/s,kr/s,kw/s,wait,actv,wsvc_t,asvc_t,%w,%b,device
    #0.1,24.8,5.2,325.9,0.0,0.0,0.0,0.4,0,0,c1t0d0
    dictlist={}
    arrtmp=[]
    tpltmp=()
    prevctime=None
    for line in fd:
        #print line
        Regex = re.compile(r'''
         (\d+)\s+(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+.*),(\d+.*),(\w+)
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)        
        if result:
            tpltmp=()
            #print ' line '+ result.group(12)
            #print line +  " and " + result.group(8)
            if float(result.group(9)) >= 1:  ##IO service time
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,13):
                        #print "Result group " + str(cnt) + " is " + result.group(cnt)
                
                        tpltmp=tpltmp + (result.group(cnt),)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp) 
                    #print "arrtmp " + str(arrtmp)
                else:
                    dictlist[prevctime]=arrtmp
                    #if prevctime =='08/01/17 20:55:45':
                    #    for lst in dictlist[prevctime]:
                    #        print "dictlist" + prevctime + " " + str(lst)
                    
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,13):
                        #print "Result group " + str(cnt) + " is " + result.group(cnt)
                
                        tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                    #arrtmp.append(result.group(0))
                #print result.group(2
                #print  ctime + "  " + result.group(2) + " " + result.group(8) 
                #print  ctime + " " + " " + result.group(2) + " " + result.group(3) + " " + result.group(4) + " " + result.group(5)   + "   " + result.group(8) +"  " + result.group(10) + "  " + result.group(11)#

    print "dict"
    print "from " + fr.ctime() + ' to ' + upto.ctime()
    print "r/s,w/s,kr/s,kw/s,wait,actv,wsvc_t,asvc_t,%w,%b,device"
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#

        #if int(key) >= int(dt_to_epoch(fr)) and int(key) <= int(dt_to_epoch(upto)):
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                #print str(it[0])
                
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print "key  " + str(key) + "  " + str(it)
                print  ctime + " " + str(float(it[2])) + " " + str(float(it[3]))  + " " + str(float(it[4])) + " " + str(float(it[5]))   + "   " + str(float(it[6])) + "  " + str(float(it[7]))+ "  " + str(float(it[8])) +"  " + it[9] + " " +  it[10]  
                #print  ctime + " " + it[11]




def dt_to_epoch(dttime):
    epoch = datetime.datetime.utcfromtimestamp(0)
    tstamp=(dttime - epoch).total_seconds()
    #return str(tstamp).split('.')[0]
    return tstamp

fr=datetime.datetime(2017,8,2,0,0,0)
#frstr=datetime.datetime.fromtimestamp(fr).strftime('%c')
upto=datetime.datetime(2017,8,2,10,0,0)
#uptostr=datetime.datetime.fromtimestamp(upto).strftime('%c')


find_iostat(fd)
#find_cpu(fd)
#find_nicstat(fd)

def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -C for CPU utilization"
    print os.path.basename(sys.argv[0]) + " -I for IO utilization  "
   
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "CI")
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
                if o == "-h":
                        usage()
                        sys.exit(0)
                elif o == "-C":
                    find_cpu()
                elif o == "-R":
                    find_iostat();
                    
                    
#if __name__ == "__main__":
    main()  
