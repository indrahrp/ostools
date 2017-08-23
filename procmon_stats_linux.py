import re
import datetime,getopt



#fd=open('C:\temp\wrk.txt')

#fd=open("c:\\temp\\testfile",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.fri",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.thu",'r')

#fd=open("C:\\temp\\temp\sysinfo_tkz2_wed")
#fd=open("c:\\temp\\temp\\sysinfo.tickz2real.fri")
fd=open("C:\\temp\\temp\sysinfo.ticksz1.thu")



#    print line
#for line in fd:
#    print line
#str1=fd.read()   
#print str
#print str1

def find_cpu(fd):
    i=0
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
            if float(result.group(11)) <= 60 :
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                #print result.group(2,11)
                print result.group(0)
                #print result.group(2)
                print  ctime + "  " + result.group(2) + " " + result.group(11)
                i=i+1
                if i==100:
                    raw_input('enter')
                
            #   intlist.append(listtmp)
            
                #return intlist

def find_nicstat(fd):
    i=0
    for line in fd:
        Regex = re.compile(r'''
        (\d+)\s+(\d+):(\w+|\w+.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+.\d+)\:(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+) 
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)        
        
        if result:
            #print "resut "+result.group(0)
            #if float(result.group(5)) > 5300 and result.group(3).strip() == 'p3p1':
            #if result.group(3).strip() == 'p3p1':
            
            if float(result.group(4)) > 1000:
            
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
    for line in fd:
        #print line
        Regex = re.compile(r'''
         (\d+)\s+(sd\w+|dm-\d),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+)
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        #print str2
        result=Regex.search(line)        
        if result:
            #print " Device:          rrqm/s   wrqm/s     r/s     w/s   rsec/s   wsec/s avgrq-sz avgqu-sz   await  svctm  %util"
            #print "sdb               0.00     0.00    0.00    0.00     0.01     0.01    13.75     0.00    5.29   5.27   0.00"
            #print result.group(0)
            #print "result " + result.group(0)
            if float(result.group(12)) > 10 :
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                #print result.group(2,11)
                #print result.group(2)
                #print  ctime + "  " + result.group(2) + " " + result.group(8) 
                print  ctime + "  " + result.group(2) + "    " + result.group(7)  + "   " + result.group(8) +"  " + result.group(12) + "  " + result.group(13)#



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
