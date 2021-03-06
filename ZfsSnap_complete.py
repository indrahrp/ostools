#!/usr/bin/env python

import getopt,sys,os,re
import subprocess,re,pprint,csv,time,datetime
from functools import partial




def snap_suffix(zfsvol):
    tm=time.localtime()
    suffix=str(tm.tm_year) +'_' + str(tm.tm_mon) + '_' +  str(tm.tm_mday) + '_' + str(tm.tm_hour) + '_'+  str(tm.tm_min) + '_' + str(tm.tm_sec)
    print 'suffix ' + suffix


def del_old_snapshot(zfsvol):
    dictsnap={}
    listsnap=[]
    listdt=[]
    command = 'zfs list -rt snapshot ' + zfsvol
    old_snapshot=exec_command(command)
    print "old _snapshot " + old_snapshot
    snaplist=[ snap.split('@') for snap in old_snapshot.split() if zfsvol + '@' in snap ] 


    print 'snaplist ' + str(snaplist)
    #snaplistdt = [[s or datetime.datetime(s) for s in snapls if zfsvol not in s] for snapls in snaplist]
    for snap,snapdt in snaplist:
	print 'snap 1 ' + snapdt
	match = re.search(r'\d+_\d+_\d+_\d+_\d+_\d+', snapdt)
	if match:
                
		(year,month,day,hour,min,sec)=snapdt.split('_')
		conv_snapdt = datetime.datetime(int(year),int(month),int(day),int(hour),int(min),int(sec))
		print " " + str(conv_snapdt)
		dictsnap[conv_snapdt]=[snap,snapdt]
                 

    #print 'dict snap ' + str(dictsnap.sort(k)
    dkeys=sorted(dictsnap)
    del_keys=dkeys[4:-1]
    for key in del_keys:
	print "key " + " " + str(key) + ' with ' + str(dictsnap[key][0])+'@'+str(dictsnap[key][1])
        
    print "to delete " + str(dkeys[4:-1])
    
    for key,value in dictsnap.items():
	print 'key is ' + str(key) + ' adn ' + str(value)
        listdt.append(key)
    idx=0
    idxl=0
    

    #listdt=[5,9,6,1,23,33,3,12,7,8,1,3,1000,4,23,21] 
    while idxl <  (len(listdt) ):
         #idxl=idxl + 1 
         idx=idxl + 1
         print "idxl lg is " + str(idxl) + " and idx " + str(idx)
   	 while idx <  (len(listdt) ):
         	print "idxl is " + str(idxl) + " and idx " + str(idx)
       		if listdt[idxl] > listdt[idx]:
                        print "listdt " + str(listdt[idxl]) + " and " + str(listdt[idx])
			tmp=listdt[idxl]
	       	        tmp1=listdt[idx]
			listdt[idx]=tmp
                	listdt[idxl]=tmp1
	       	idx=idx+1

         idxl=idxl + 1 
    print "list to delete dt " + str(listdt[4:-1])
    for dt in listdt[4:-1]:
	print str(dt) + " with zfs name " + str(dictsnap[dt][0]+'@'+dictsnap[dt][1] )  

    
def exec_command(command):
        print "executing command :  " + command        
        active_link=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines=active_link.communicate()
        print "Output " + lines[0]
        print "Error " + lines[1]
        return lines[0]
        

cmd_list_zfs_snapshot=[
            'zfs snapshot + svcadm enable /system/name-service-cache'
    ]

        
def restofcommand():
     for cmd in cmd_list_rest:
        exec_command(cmd)
          
def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -S zfs volume  -D number of snapshot to keep"
    print "\nFor example : " + os.path.basename(sys.argv[0]) + " -S home/packages -D 4 "
    
    
def main():
    zfsvol=None
    keep=None
    opts=None
    args=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "S:D:h")
        print str(opts)
    except getopt.GetoptError as err:
        print str(err)
        usage()
	sys.exit(0)
              
    for o,a in opts:
                print ' o is ' + o
                if o == "-h":
                        usage()
                        sys.exit(0)
                elif o == "-S":
                    zfsvol=a
                elif o == "-D":
                    keep=a
                else:
                    print " incorrect option "
                    sys.exit(0)
    #print "zfs vol " + zfsvol + " and keep " + keep
    if zfsvol and keep:                
        suffix=snap_suffix(zfsvol)
        del_old_snapshot(zfsvol)
        
    
    

if __name__ == "__main__":
        main()  

