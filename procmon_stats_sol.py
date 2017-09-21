import re
import datetime,getopt
from collections import OrderedDict
from time import ctime



#fd=open('C:\temp\wrk.txt')

#fd=open("c:\\temp\\testfile",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.fri",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.thu",'r')
#fd=open("C:\\temp\\temp\\sysinfo.tue.itfpecz2b")
fd=open("C:\\temp\\temp\\sysinfo.wed.vabdbx2")

#fd=open("C:\\temp\\temp\\sysinfo.mon.mashiez2a")

#fd=open("C:\\temp\sysinfo2.wed")

def find_prstat(fd):
    #1503374589  25627 snmp     0.2 0.4 0.0 0.0 0.0 0.0  99 0.0   4   0  2K   1 proxyagent.5/1    
    #  PID USERNAME USR SYS TRP TFL DFL LCK SLP LAT VCX ICX SCL SIG PROCESS/NLWP
    #  12466 root     0.4 0.6 0.0 0.0 0.0 0.0  99 0.0  93   5 739   0 snmpd/1

    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing for prstat  line" + str(cntr)
                                        
        Regex = re.compile(r'''
        (\d+)\s+(\d+)\s+(\w+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+([\d.]+)\s+
        ([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+
        (\d+)\s+(\w+)\s+(\w+)\s+([\w./]+)
        #(\d+)\s+(\w+)(\w+)\s+(\d+)\s+(.*)$
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)
        if result:
            #print 'result0 ' + result.group(0)
            #raw_input('')
            #if  'ETG' in result.group(16):
            #    print "ETG is " + result.group(0)
            #    raw_input('')
            tpltmp=()
            if float(result.group(11)) >= 0 and 'gtp' in result.group(3) :
                print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,17):           
                        tpltmp=tpltmp + (result.group(cnt),)
                        #print "tpltmp " + str(tpltmp)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp) 
                else:
                    dictlist[prevctime]=arrtmp
                    #print dictlist[prevctime]
                    #raw_input('ss prompt')
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,17):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print fr.ctime() + ' to ' + upto.ctime()
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:18s} {:8s} {:10s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:15s}'.format('Date Time','PID','USERNAME', 'USR', 'SYS', 'TRP', 'TFL', 'DFL', 'LCK', 'SLP','LAT','VCX','ICX','SCL','SIG','PROCESS/NLWP' )
    
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                # print ctime + "  " +  "   ".join(it)
                #print  ctime + " " + str(it[])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[15]))  
                #print (it[0],it[1],it[2],it[15])
                print '{:18s} {:8s} {:10s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:15s}'.format(ctime,it[0],it[1],it[2],it[3],it[4],it[5], \
                it[6],it[7],it[8],it[9],it[10],it[11],it[12],it[13],it[14])
                                                            
                #print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
            
                #print " ::".join(it)
                i=i+1
                if i==30:
                    raw_input('')
                    #print '{:18s} {:8s} {:10s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s}{:5s} {:15s}'.format('Date Time','PID','USERNAME', 'USR', 'SYS', 'TRP', 'TFL', 'DFL', 'LCK', 'SLP','LAT','VCX','ICX','SCL','SIG','PROCESS/NLWP' )
                    #print '{:18s} {:8s} {:10s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:15s}'.format('Date Time','PID','USERNAME', 'USR', 'SYS', 'TRP', 'TFL', 'DFL', 'LCK', 'SLP','LAT','VCX','ICX','SCL','SIG','PROCESS/NLWP' )
                    print '{:18s} {:8s} {:10s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:15s}'.format('Date Time','PID','USERNAME', 'USR', 'SYS', 'TRP', 'TFL', 'DFL', 'LCK', 'SLP','LAT','VCX','ICX','SCL','SIG','PROCESS/NLWP' )
  
                    i=0
    
def find_cpustat(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing for cpustat  line" + str(cntr)
                                        
        Regex = re.compile(r'''
        (\d+)\s+(\d{1,2})\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+ 
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+$
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)
        if result:
            tpltmp=()
            tstamp=float(result.group(1))
            ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
            print result.group(0) + 'with ' + ctime
            if float(result.group(17)) <= 70:
                print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,18):           
                        tpltmp=tpltmp + (result.group(cnt),)
                        #print "tpltmp " + str(tpltmp)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp) 
                else:
                    dictlist[prevctime]=arrtmp
                    print dictlist[prevctime]
                    #raw_input('ss prompt')
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,18):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print fr.ctime() + ' to ' + upto.ctime()
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:18s} {:4s} {:5s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s}{:5s}'.format('Date Time','CPU', 'minf', 'mjf', 'xcall','intr','ithr',  'csw', 'icsw', 'migr', 'smtx', 'srw', 'syscl',  'usr', 'sys','st','idle' )
    
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                # print ctime + "  " +  "   ".join(it)
                #print  ctime + " " + str(it[])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[15]))  
                #print (it[0],it[1],it[2],it[15])
                print '{:18s} {:4s} {:5s} {:5s} {:5s} {:6s} {:6s} {:6s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s} {:5s}'.format(ctime,it[0],it[1],it[2],it[3],it[4],it[5], \
                it[6],it[7],it[8],it[9],it[10],it[11],it[12],it[13],it[14],it[15])
                                                            
                #print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
            
                #print " ::".join(it)
                i=i+1
                if i==30:
                    raw_input('')
                    i=0
                                
def find_vmstat(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing line for vmstat " + str(cntr)
                                        
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
        result=Regex.search(line)
        if result:
            tpltmp=()
            if float(result.group(23)) <= 100:
                print result.group(23)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,24):           
                        tpltmp=tpltmp + (result.group(cnt),)
                        #print "tpltmp " + str(tpltmp)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp) 
                else:
                    dictlist[prevctime]=arrtmp
                    print dictlist[prevctime]
                    #raw_input('ss prompt')
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,24):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print  fr.ctime() + ' to ' + upto.ctime()
    #print "CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl"
    #print " kthr      memory            page            disk          faults      cpu"
    #print "r b w   swap  free  re  mf pi po fr de sr s0 s1 s2 s3   in   sy   cs us sy id"
    
    # kthr      memory            page            disk          faults      cpu
    #r b w   swap  free  re  mf pi po fr de sr s0 s1 s2 s3   in   sy   cs us sy id
    #0 0 0 513978512 485625476 768 2477 0 0 0 0 0 26 26 18 17 23883 38802 22080 0 1 99

    print '{:18s} {:2s} {:2s} {:2s} {:10s} {:10s} {:5s} {:5s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:4s} {:6s} {:6s} {:6s} {:3s} {:3s} {:3s} '.\
    format('Date Time','r','b','w','swap','free','re','mf','pi','po','fr','de','sr','s0','s1','s2','s3','in','sy','cs','us','sy','id')
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print  ctime + "  " + result.group(2) + " " + result.group(23)
                #print  ctime + " " + str(float(it[2])) + " " + str(float(it[23]))  + " " + str(float(it[4])) + " " + str(float(it[5]))   + "   " + str(float(it[6])) + "  " + str(float(it[7]))+ "  " + str(float(it[8])) +"  " + it[9] + " " +  it[10]  
                #print "    ".join(it)
                #print  ctime + " " + str(float(it[2])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[21]))  
                #print '{:18s} {:10s} {:10s} {:18s} {:10s}'.format(ctime,it[0],it[2],it[4],it[6],it[21])
                print '{:18s} {:2s} {:2s} {:2s} {:10s} {:10s} {:5s} {:5s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:4s} {:3s} {:6s} {:6s} {:6s} {:3s} {:3s} {:3s} '.\
                format(ctime,it[0],it[1],it[2],it[3],it[4],it[5],it[6],it[7],it[8],it[9],it[10],it[11],it[12],it[13],it[14],it[15],it[16],it[17],it[18],it[19],it[20],it[21])
                i=i+1
                if i==30:
                    raw_input('')
                    print '{:18s} {:2s} {:2s} {:2s} {:10s} {:10s} {:5s} {:5s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:3s} {:4s} {:6s} {:6s} {:6s} {:3s} {:3s} {:3s} '.\
                    format('Date Time','r','b','w','swap','free','re','mf','pi','po','fr','de','sr','s0','s1','s2','s3','in','sy','cs','us','sy','id')
   
                    i=0
                 
def find_nicstat(fd):
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        cntr=cntr+1
        print "processsing line for nicstat " + str(cntr)
        Regex = re.compile(r'''
        (\d+)\s+(\d+):(\w+|\w+.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+)\:(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+) 
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)        
        
        if result:
            #print result.group(0)
            tpltmp=()
            #print result.group(0)
            if float(result.group(4)) >= 500:
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(3,6):           
                        tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                else:
                    dictlist[prevctime]=arrtmp
                    #print dictlist[prevctime]
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(3,6):
                           tpltmp=tpltmp + (result.group(cnt),)
                    #print tpltmp
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print fr.ctime() + ' to ' + upto.ctime()
    print " TIME              INT      rKB/s   wKB/s"
    for key,item in dictlist.items():
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print ctime + "  " +  "   ".join(it)
                #if it[0] == 'net9.1702':
                if it[0]:
                
                    print '{:18s} {:10s} {:10s} {:10s} '.format(ctime,it[0],it[1],it[2])
                                                           
                    #print  ctime + "  " + result.group(3) + "    " + result.group(4)  + \
                    #"   " + result.group(5)
                    i=i+1
                    if i==30:
                        raw_input('')
                        i=0

def find_iostat(fd):
    #r/s,w/s,kr/s,kw/s,wait,actv,wsvc_t,asvc_t,%w,%b,device
    #0.1,24.8,5.2,325.9,0.0,0.0,0.0,0.4,0,0,c1t0d0
    dictlist=OrderedDict()
    i=0
    arrtmp=[]
    tpltmp=()
    prevctime=None
    cntr=0
    for line in fd:
        cntr=cntr + 1
        print "processsing line for iostat " + str(cntr)
        Regex = re.compile(r'''
         (\d+)\s+(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+.*),(\d+.*),(\w+)
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)        
        if result:
            tpltmp=()
            if float(result.group(9)) >= 2:  ##IO service time
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,13):           
                        tpltmp=tpltmp + (result.group(cnt),)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp)
                 
                    #print "arrtmp " + str(arrtmp)
                else:
                    dictlist[prevctime]=arrtmp
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,13):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print  fr.ctime() + ' to ' + upto.ctime()
    print '{:18s} {:8s} {:10s} {:8s} {:8s} {:6s} {:6s} {:6s} {:8s} {:5s} {:5s} {:5s}'.format("Date Time","r/s","w/s","kr/s","kw/s","wait","actv","wsvc_t","asvc_t","%w","%b","device")
   
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#

        #if int(key) >= int(dt_to_epoch(fr)) and int(key) <= int(dt_to_epoch(upto)):
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                #print str(it[0])
                
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print "key  " + str(key) + "  " + str(it)
                #print  ctime + " " + str(float(it[2])) + " " + str(float(it[3]))  + " " + str(float(it[4])) + " " + str(float(it[5]))   + "   " + str(float(it[6])) + "  " + str(float(it[7]))+ "  " + str(float(it[8])) +"  " + it[9] + " " +  it[10]  
                #print  ctime + " " + it[11]
                print '{:18s} {:8s} {:10s} {:8s} {:8s} {:6s} {:6s} {:6s} {:8s} {:5s} {:5s} {:5s}'.format(ctime,it[0],it[1],it[2],it[3],it[4],it[5], \
                it[6],it[7],it[8],it[9],it[10])
                i=i+1
                if i==30:
                    raw_input('')
                    print '{:18s} {:8s} {:10s} {:8s} {:8s} {:6s} {:6s} {:6s} {:8s} {:5s} {:5s} {:5s}'.format("Date Time","r/s","w/s","kr/s","kw/s","wait","actv","wsvc_t","asvc_t","%w","%b","device")
   
                    i=0


def dt_to_epoch(dttime):
    togettoest=datetime.timedelta(seconds=14400) 
    epoch = datetime.datetime.utcfromtimestamp(0) - togettoest
    tstamp=(dttime - epoch).total_seconds()
    #return str(tstamp).split('.')[0]
    return tstamp

fr=datetime.datetime(2017,8,30,9,00,0)
#frstr=datetime.datetime.fromtimestamp(fr).strftime('%c')
upto=datetime.datetime(2017,8,30,10,10,0)
#uptostr=datetime.datetime.fromtimestamp(upto).strftime('%c')


find_iostat(fd)
#find_vmstat(fd)
#find_cpustat(fd)
#find_nicstat(fd)
find_prstat(fd)
fd.close()
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
