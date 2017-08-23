import re
import datetime,getopt
from collections import OrderedDict
from time import ctime



#fd=open('C:\temp\wrk.txt')

#fd=open("c:\\temp\\testfile",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.fri",'r')
#fd=open("C:\Users\uc205955\Downloads\sysinfo.thu",'r')
#fd=open("C:\\temp\\temp\\sysinfo.ticksz2.thu1")
fd=open("C:\\temp\\temp\\sysinfo.wed.tickz1-0823a ")

#fd=open("C:\\temp\\temp\\sysinfo_tkz2_wed1")
#fd=open("C:\\temp\\temp\\sysinfo_tkz2_fri1")
#fd=open("C:\\temp\\temp\\sysinfo_tkz2_fri")
#fd=open("c:\\temp\\temp\\sysinfo.tickz2realtmp.fri")

#fd=open("C:\\temp\sysinfo2.wed")






def find_cpustat(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    #1502866801 1 26.88 0.00 10.75 0.00 0.00 6.45 0.00 0.00 55.91
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
        (\d+)\s+(\d{1,2})\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+
        (\d+\.\d+)\s+(\d+\.\d+)\s+$
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)
        if result:
            tpltmp=()
            if float(result.group(11)) <= 85:
                print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,12):           
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
                    for cnt in range(2,12):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print fr.ctime() + ' to ' + upto.ctime()
    #13:49:36     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:18s} {:4s} {:5s} {:5s} {:5s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Date Time','CPU', '%usr', '%nice', '%sys','%ioswait','%irq', '%soft', '%steal', '%guest', '%idle')
    
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                # print ctime + "  " +  "   ".join(it)
                #print  ctime + " " + str(it[])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[15]))  
                #print (it[0],it[1],it[2],it[15])
                print '{:18s} {:4s} {:5s} {:5s} {:5s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format(ctime,it[0],it[1],it[2],it[3],it[4], \
                it[5],it[6],it[7],it[8],it[9])
                                                            
                #print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
        
                
                i=i+1
                if i==30:
                    raw_input('enter')
                    print '{:18s} {:4s} {:5s} {:5s} {:5s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Date Time','CPU', '%usr', '%nice', '%sys','%ioswait','%irq', '%soft', '%steal', '%guest', '%idle')
                    i=0
                                
def find_vmstat(fd):
    print "procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----"
    print " r  b    swpd   free   buff   cache     si   so    bi    bo   in   cs      us    sy  id  wa  st "

    #      18  0      0 119052816 460268 7515760    0    0     0     0  20343 181871  3      2  95  0   0"

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
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+ 
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+(\d+)\s+(\d+)\s+
        (\d+)\s+$
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)
        if result:
            print result.group(0)
            tpltmp=()
            if float(result.group(5)) <= 140000000:
                #print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,19):           
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
                    for cnt in range(2,19):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print   fr.ctime() + ' to ' + upto.ctime()
    #print "procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----"
    #print " r  b    swpd   free   buff   cache     si   so    bi    bo   in   cs      us    sy  id  wa  st "
    print '{:18s} {:4s} {:4s} {:12} {:12s} {:10s} {:10s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} '.format(' Date Time', 'r',  'b','swpd','free','buff','cache','si','so','bi','bo',\
    'in','cs','us','sy','id','wa','st')
                   
    #      18  0      0 119052816 460268 7515760    0    0     0     0  20343 181871  3      2  95  0   0"

    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print  ctime + "  " + result.group(2) + " " + result.group(23)
                #print  ctime + " " + str(float(it[2])) + " " + str(float(it[23]))  + " " + str(float(it[4])) + " " + str(float(it[5]))   + "   " + str(float(it[6])) + "  " + str(float(it[7]))+ "  " + str(float(it[8])) +"  " + it[9] + " " +  it[10]  
            
                #print(str(it))#print (it[0],it[1],it[2],it[15])
                print '{:18s} {:4s} {:4s} {:12s} {:12s} {:10s} {:10s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} '.format(ctime,it[0],it[1],it[2],it[3],it[4], \
                it[5],it[6],it[7],it[8],it[9],it[10],it[11],it[12],it[13],it[14],it[15],it[16])
                                              #print  ctime + " " + str(float(it[2])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[16]))  
                #print ' '.join(it)
                
                i=i+1
                if i==30:
                    raw_input('enter')
                    print '{:18s} {:4s} {:4s} {:12} {:12s} {:10s} {:10s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} '.format('Date Time', 'r',  'b','swpd','free','buff','cache','si','so','bi','bo',\
    'in','cs','us','sy','id','wa','st')
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
        #print "processsing line for nicstat " + str(cntr)
        Regex = re.compile(r'''
        (\d+)\s+(\d+):(\w+|\w+.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+.\d+)\:(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+):(\d+\.\d+):
        (\d+\.\d+):(\d+\.\d+) 
        ''',re.IGNORECASE | re.VERBOSE )
        #print(str)#print "sting ins" + str1
        result=Regex.search(line)        
        
        if result:
            tpltmp=()
            #print result.group(0)
            if float(result.group(4)) >= 1000:
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
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
    print  fr.ctime() + ' to ' + upto.ctime()
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
                        raw_input('enter')
                        i=0





def find_iostat(fd):
    #r/s,w/s,kr/s,kw/s,wait,actv,wsvc_t,asvc_t,%w,%b,device
    #0.1,24.8,5.2,325.9,0.0,0.0,0.0,0.4,0,0,c1t0d0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    cntr=0
    for line in fd:
        cntr=cntr + 1
        print "processsing line for iostat " + str(cntr)
        Regex = re.compile(r'''
        (\d+)\s+(sd\w+|dm-\d),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+),(\d+\.\d+),(\d+\.\d+),
        (\d+\.\d+)
        ''',re.IGNORECASE | re.VERBOSE )
        result=Regex.search(line)        
        if result:
            tpltmp=()
            print result.group(0)
            if float(result.group(12))>= 2:  ##IO service time
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,14):           
                        tpltmp=tpltmp + (result.group(cnt),)
                    #print " tplmp "+ str(tpltmp)
                    arrtmp.append(tpltmp)
                 
                    #print "arrtmp " + str(arrtmp)
                else:
                    dictlist[prevctime]=arrtmp
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,14):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print  fr.ctime() + ' to ' + upto.ctime()
    print '{:18s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:8s} {:8s} {:8s}'.format("Date Time","Device","rrqm/s","wrqm/s","r/s","w/s","rsec/s","wsec/s","avgrq-sz", "avgqu-sz","await","svctm","%util")
    #print " Device:          rrqm/s   wrqm/s     r/s     w/s   rsec/s   wsec/s avgrq-sz avgqu-sz   await  svctm  %util"
    #print "sdb               0.00     0.00    0.00    0.00     0.01     0.01    13.75     0.00    5.29   5.27   0.00"
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
                #print  ctime + "  " + result.group(2) + "    " + result.group(7)  + "   " + result.group(8) +"  " + result.group(12) + "  " + result.group(13)##print  ctime + " " + it[11]
                #print '{:18s} {:10s} {:10s} {:10s} '.format(ctime,it[0],it[1],it[2])
                print '{:18s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:8s} {:8s} {:8s}'.format(ctime,it[0],it[1],it[2],it[3],it[4], \
                it[5],it[6],it[7],it[8],it[9],it[10],it[11])





def find_topstat(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    #1502866801 1 26.88 0.00 10.75 0.00 0.00 6.45 0.00 0.00 55.91
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing for topstat  line" + str(cntr)
        
        Regex = re.compile(r'''  
        (\d+)\s+(\d+)\s+(\w+)\s+(\d+)\s+(\d+)\s+
        (\w+)\s+(\w+)\s+([a-zA-Z]+)\s+([:.0-9a-zA-Z]+)\s+([0-9.%]+)\s+([0-9.%]+)\s+(\w+)
        ''',re.IGNORECASE | re.VERBOSE )

                 
       
        result=Regex.search(line)
        if result:
            print result.group(0)
            tpltmp=()
            if float(result.group(4)) >= 5:
                print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,13):           
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
                    for cnt in range(2,13):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print  fr.ctime() + ' to ' + upto.ctime()
    #13:49:36     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:18s} {:8s} {:8s} {:4s} {:4s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Date Time','PID','USERNAME', 'PRI', 'NICE',  'SIZE','RES', 'STATE','TIME','WCPU','CPU','COMMAND')
    
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                # print ctime + "  " +  "   ".join(it)
                #print  ctime + " " + str(it[])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[15]))  
                #print (it[0],it[1],it[2],it[15])
                print '{:18s} {:8s} {:8s} {:4s} {:4s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format(ctime,it[0],it[1],it[2],it[3],it[4], \
                it[5],it[6],it[7],it[8],it[9],it[10])
                                                            
                #print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
        
                
                i=i+1
                if i==30:
                    raw_input('enter')
                    #print '{:18s} {:4s} {:5s} {:5s} {:5s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Date Time','CPU', '%usr', '%nice', '%sys','%ioswait','%irq', '%soft', '%steal', '%guest', '%idle')
                    print '{:18s} {:8s} {:8s} {:4s} {:4s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s}'.format('Date Time','PID','USERNAME', 'PRI', 'NICE',  'SIZE','RES', 'STATE','TIME','WCPU','CPU','COMMAND')
                    i=0
                                


def find_loadaverage(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    #1502866801 1 26.88 0.00 10.75 0.00 0.00 6.45 0.00 0.00 55.91
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing for load Average line" + str(cntr)
        #print line
        
        Regex = re.compile(r'''         
        (\d+).*load\s+avg:\s+([0-9.]+).*([0-9.]).*([0-9.]).*up   
        ''',re.IGNORECASE | re.VERBOSE |re.DOTALL )

                 
       
        result=Regex.search(line)
        if result:
            #print result.group(0)
            tpltmp=()
            if float(result.group(2)) >= 0:
                #print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,5):           
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
                    for cnt in range(2,5):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print  fr.ctime() + ' to ' + upto.ctime()
    #13:49:36     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:^18s} {:^10s} {:^10s} {:^10s}'.format('Date Time','1MinLoad ', '5MinLoad', '15MinLoad')
    
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                # print ctime + "  " +  "   ".join(it)
                #print  ctime + " " + str(it[])) + " " + str(float(it[4])) + " "+ str(float(it[6])) + " " + str(float(it[15]))  
                #print (it[0],it[1],it[2],it[15])
                print '{:^18s} {:^10s} {:^10s} {:^10s} '.format(ctime,it[0],it[1],it[2])
                                                            
                #print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
        
                
                i=i+1
                if i==30:
                    raw_input('enter')
                    #print '{:18s} {:10s} {:10s} {:10s}'.format('Date Time','1 Minute Load ', '5 Minute Load', '15 Minute Load')
                    print '{:^18s} {:^10s} {:^10s} {:^10s}'.format('Date Time','1MinLoad ', '5MinLoad', '15MinLoad')
                    i=0
                                

def find_cpustates(fd):
    ## CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl
    ##  0   64   0    0   511  211  248   11    0    0    0  1056    1   2   0  97
    #1502866801 1 26.88 0.00 10.75 0.00 0.00 6.45 0.00 0.00 55.91
    i=0
    cntr=0
    dictlist=OrderedDict()
    arrtmp=[]
    tpltmp=()
    prevctime=None
    
    for line in fd:
        intlist=[]  
        cntr=cntr+1  
        print "processsing for cpustates line" + str(cntr)
        #print line
        
        Regex = re.compile(r'''         
        (\d+)\s+CPU\s+states:\s+([0-9.%]+)\s+user,\s+([0-9.%]+)\s+nice,\s+([0-9.%]+)\s+system,\s+([0-9.%]+)\s+idle,\s+([0-9.%]+)\s+iowait
        ''',re.IGNORECASE | re.VERBOSE )

                 
       
        result=Regex.search(line)
        if result:
            #print  result.group(0)
            #print  result.group(2),result.group(3),result.group(4),result.group(5),result.group(6)
            tpltmp=()
            #print result.group(4)
            # system > .. %
            #print result.group(3).rstrip('%')
            if float(result.group(2).rstrip('%')) >= 1:
                #print result.group(0)
                #raw_input('ss prompt')
                tstamp=float(result.group(1))
                ctime=datetime.datetime.fromtimestamp(tstamp).strftime('%c')
                if not prevctime:
                    prevctime=tstamp
                if tstamp==prevctime:
                    for cnt in range(2,7):           
                        tpltmp=tpltmp + (result.group(cnt),)
                    
                    arrtmp.append(tpltmp) 
                else:
                    dictlist[prevctime]=arrtmp
                    #print dictlist[prevctime]
                    #raw_input('ss prompt')
                    prevctime=tstamp
                    arrtmp=[]
                    for cnt in range(2,7):
                           tpltmp=tpltmp + (result.group(cnt),)
                    arrtmp.append(tpltmp) 
                   
    #print "dict"
    print fr.ctime() + ' to ' + upto.ctime()
    #13:49:36     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
    #print "Date Time CPU minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  st idl "
    print '{:18s} {:10s} {:10s} {:10s} {:10s} {:10s}'.format('Date Time','%User ', 'Nice','%System', '%Idle', '%Iowait')
    # output will be 1502426782 CPU states:  1.4% user,  0.0% nice,  0.9% system, 97.7% idle,  0.0% iowait
    for key,item in dictlist.items():
        #print  ctime + " atas " + it[2] + " " + it[3]  + " " + it[4] + " " + it[5]   + "   " + it[8] +"  " + it[10] + "  " + it[11]#
        if key >= dt_to_epoch(fr) and key <= dt_to_epoch(upto):
            #print str(item)
            for it in item:
                ctime=datetime.datetime.fromtimestamp(key).strftime('%c')
                #print "  ".join(it)
                print '{:18s} {:10s} {:10s} {:10s} {:10s} {:10s} '.format(ctime,it[0],it[1],it[2],it[3],it[4])
      
                i=i+1
                if i==30:
                    raw_input('enter')
                    print '{:18s} {:10s} {:10s} {:10s} {:10s} {:10s}'.format('Date Time','%User ', 'Nice','%System', '%Idle', '%Iowait')
                    i=0
                                


def dt_to_epoch(dttime):
    togettoest=datetime.timedelta(seconds=14400) 
    epoch = datetime.datetime.utcfromtimestamp(0) - togettoest
    tstamp=(dttime - epoch).total_seconds()
    #return str(tstamp).split('.')[0]
    return tstamp

fr=datetime.datetime(2017,8,22,23,30,0)
#frstr=datetime.datetime.fromtimestamp(fr).strftime('%c')
upto=datetime.datetime(2017,8,23,0,2,0)
#uptostr=datetime.datetime.fromtimestamp(upto).strftime('%c')


#find_iostat(fd)
#find_vmstat(fd)
#find_cpustat(fd) 
#find_nicstat(fd)
#find_topstat(fd)
#find_loadaverage(fd)
find_cpustates(fd)

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
