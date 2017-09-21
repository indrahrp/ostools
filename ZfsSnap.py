#!/bin/env python

import getopt,sys,os,re
import subprocess,re,pprint,csv,time
from numpy.distutils.fcompiler import none


backupdir='/var/tmp/pkgbck/'


def snap_suffix(zfsvol):
    tm=time.localtime()
    suffix=tm.tm_year +'_' + tm.tm_mon + '_' +  tm.tm_mday + '_' + tm.tm_hour + '_'+  tm.tm_min + '_' + tm_sec
    print 'suffix ' + suffix
    
def exec_command(command):
        print "executing command :  " + command        
        active_link=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines=active_link.communicate()
        print "Output " + lines[0]
        print "Error " + lines[1]
        
        

cmd_list_zfs_snapshot=[
            
            ''
            'svcadm enable svc:/network/nfs/status:default svc:/network/nfs/nlockmgr:default svc:/network/nfs/mapid:default svc:/network/nfs/client:default svc:/network/nfs/rquota:default', 
            'svcadm restart autofs',
            'svcadm enable /system/name-service-cache'
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
    except getopt.GetoptError as err:
        print str(err)
        usage()
              
    for o,a in opts:
                print ' o is ' + o
                if o == "-h":
                        usage()
                        sys.exit(0)
                if o == "S":
                    zfsvol=a
                if o == "D":
                    keep=a
                else:
                    print " incorrect option "
                    sys.exit(0)
    print "zfs vol " + zfsvol + " and keep " + keep
    if zfsvol and keep:                
        snap_suffix(zfsvol)
    
    

if __name__ == "__main__":
        main()  

