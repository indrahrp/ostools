#!/bin/python

import getopt,sys,os,re
from collections import OrderedDict 
import subprocess,re,pprint,csv

backupdir='/var/tmp/pkgbck/'

def exec_command(command):
        print "execuing command " + command        
        #active_link=subprocess.Popen(['dladm','show-phys'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        active_link=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        lines=active_link.communicate()
        print "Output " + lines[0]
        print "Error " + lines[1]
        
cmd_list_backup=[
            'mkdir -p ' + backupdir + 'usr/local',
            'mkdir -p ' + backupdir + 'usr/pkg',
            'mkdir -p ' + backupdir + 'var/db',
            'mkdir -p ' + backupdir + 'var/bbmon',
            '(cd /usr/pkg && find . -depth -print | cpio -pdumv ' + backupdir + 'usr/pkg)',   
            '(cd /usr/local && find . -depth -print | cpio -pdumv ' + backupdir + 'usr/local)',
            '(cd /var/db && find . -depth -print | cpio -pdumv ' + backupdir + 'var/db)',
            '(cd /var/bbmon &&  find . -depth -print | cpio -pdumv ' + backupdir + 'var/bbmon)',
            '/usr/pkg/sbin/pkg_info > ' + backupdir + 'pkginfoall.txt',
            'tar cvf ' + backupdir + 'opt.tar /opt',
            'format > ' + backupdir + 'format.txt 0</dev/null',
            
            'netstat -i > ' + backupdir + 'netstatii',
            'netstat -nrv > ' + backupdir + 'netstatnrv',
            'cp /etc/inet/static_routes-DefaultFixed  ' + backupdir + 'static_routes-DefaultFixed.txt',
            'cp /etc/system ' + backupdir + 'system',
            'cp /etc/rc2.d/S68ndd ' + backupdir,    
            'cp /etc/resolv.conf ' + backupdir,
            'cp /etc/nsswitch.conf ' + backupdir,
            'cp  /etc/zephyr.servers ' + backupdir,
            'ipadm > ' + backupdir + 'ipadm',
            'dladm show-link > ' + backupdir + 'dladmshowlinks',
            'dladm show-phys -L > ' + backupdir + 'dladmshowphysL',
            'dladm show-vnic > ' + backupdir + 'dladmshowvnic',
            'ifconfig -a > ' + backupdir + 'ifconfiga',
            'cp  /etc/gateways ' + backupdir,
            'netstat -nr > ' + backupdir + 'netstatnr.txt',
            'zfs list > ' + backupdir + 'zfslist.txt',
            'zpool status > ' + backupdir + 'zpoolstatus.txt',
            'zpool list >  ' + backupdir + 'zpoollist.txt',
            'zfs get all > ' + backupdir + 'zfsgetall.txt',
            'zpool  get all gtplog > ' + 'zpoolgetallgtplog.txt',
            'zpool get all ilx > ' + 'zpoolgetallilx.txt',
            'zpool get all rpool > ' + 'zpoolgetallrpool.txt',
            'diskinfo -a  > ' + backupdir + 'diskinfo.txt',
            'date >  '+ backupdir + 'date.txt',
            'svccfg -s svc:/system/environment:init listprop environment/LANG > ' + backupdir + 'envlang.txt',
            'svccfg -s svc:/system/timezone:default listprop timezone/localtime > ' + backupdir + 'timezonelocaltime.txt',
            
            'cp /etc/hosts ' + backupdir,
            'cp /etc/services ' + backupdir,   

            'cp  /etc/vfstab ' + backupdir,
            'cp  /etc/dfs/dfstab '+ backupdir,
            '(cd /var/spool/cron;cp -r crontabs/ ' + backupdir +'crontabs)',
            'cp  /etc/sudoers ' + backupdir + 'sudoers',
            'cp  /usr/pkg/etc/sudoers ' + backupdir + 'pkgetcsudoers',
            'cp  /etc/prodeng.conf ' + backupdir + 'prodeng.conf',
            'cp  /etc/profile ' + backupdir  + 'profile',
            'cp -r /etc/profile.d ' + backupdir + 'profile.d',
            
            
            'prtdiag -v > ' + backupdir + 'prtdiagv',
            'psrinfo > ' + backupdir + 'psrinfo',
            'cp  /etc/passwd  ' + backupdir + 'passwd.txt',
            'cp  /etc/shadow  ' + backupdir + 'shadow.txt',
            'cp  /etc/group  ' + backupdir + 'group.txt',
            'cp -r /etc/ssh ' + backupdir,
            'cp -r /var/named ' + backupdir,
            'cp -r /var/yp ' + backupdir, 
            'mkdir -p /var/tmp/pkgbck/kerneldrv/ ; cp -r /kernel/drv ' + backupdir + 'kerneldrv/',
            'cp  /bps.sh ' + backupdir, 
            'cp /etc/inetd.conf ' + backupdir,
            'cp  /etc/hosts ' + backupdir + 'hosts1',
            'cp  /etc/services ' + backupdir + 'services1',
            'beadm list > ' + backupdir + 'beadmlist',
            
            
            "(cd /var/spool/cron/crontabs && for user in `ls -tlr | awk '{print $9}'|grep -v ^$`;do  echo 'USER ' $user >> ' + backupdir + 'cronbck ; cat $user >> " + backupdir + "cronbck;done)",


            
            'cp  /kernel/drv/sd.conf ' + backupdir,
            'cp  /kernel/drv/ixgbe.conf ' + backupdir,
            'cp  /kernel/drv/nxge.conf ' + backupdir,
            'cp  /kernel/drv/nge.conf ' + backupdir, 
            'cp  /kernel/drv/nxge.conf ' + backupdir, 
            'cp  /kernel/drv/igb.conf ' + backupdir, 
            'cp  /kernel/drv/igbvf.conf ' + backupdir, 



            '(mkdir -p ' + backupdir + 'ntpdir/etc/inet ; mkdir -p ' + backupdir + 'ntpdir/etc/ntp/ ;cp  /etc/inet/ntp* ' + backupdir + 'ntpdir/etc/inet;cp /etc/ntp/* ' + backupdir + 'ntpdir/etc/ntp/; cp /etc/ntp.keys  ' + backupdir + 'ntpdir/etc)',
            'pkg list entire > ' + backupdir + 'pkglistentire.txt',
            'pkg list > ' + backupdir + 'pkglist.txt',
            'svcs -a > ' + backupdir + 'svcsa.txt',
            'pkg list |grep -i idr > ' + backupdir + 'pkglistidr.txt',
            'pkginfo > ' + backupdir + 'pkginfosol10.txt',
            'zfs get -r sharenfs > ' + backupdir + 'zfsgetsharenfs.txt',
            'cp -pr /etc/dfs/ ' + backupdir + 'dfs',
            'mount > ' + backupdir + 'mount.txt',
            'zfs mount > ' + backupdir + 'zfsmount.txt',

            'biosconfig -get_bios_settings > ' + backupdir + 'bios_configbef.xml',

            'ubiosconfig export  all -x ' + backupdir + 'biosconfigbef.xml',

            
            
            'netstat -ni > ' + backupdir + 'netstatni.txt',
           ]



cmd_list_restore=[
            'mkdir /etc/sysadmin && (mv /etc/inet/hosts /etc/inet/services /etc/sysadmin/;ln -s /etc/sysadmin/hosts /etc/inet/hosts;ln -s /etc/sysadmin/services /etc/inet/services)',
            'cp ' + backupdir + 'system /etc/',
            '(cp ' + backupdir + 'S68ndd /etc/rc2.d && chmod /etc/rc2.d/S68ndd)',
            'cp ' + backupdir +'resolv.conf /etc/',
            'cp ' + backupdir  + 'nsswitch.conf /etc/',
            'cp ' + backupdir + 'zephyr.servers /etc/',
            'cp ' + backupdir + 'gateways /etc/',
            
            "cat " + backupdir + "envlang.txt | awk '{print $3}' | xargs svccfg -s svc:/system/environment:init setprop environment/LANG = astring:",
            'svcadm refresh svc:/system/environment:init',
            "cat " + backupdir + "timezonelocaltime.txt |awk '{print $3}'| xargs  svccfg -s svc:/system/timezone:default setprop timezone/localtime= astring:",
            'svcadm refresh svc:/system/timezone:default',
            
            'cp ' + backupdir + 'hosts /etc/sysadmin/hosts',
            'cp ' + backupdir + 'services /etc/sysadmin/services',
            
             "(cd " + backupdir + "crontabs;for user in `ls |egrep -vi '(root|sys|adm|lp|snmp)'`;do  cp $user /var/spool/cron/crontabs;done)",
            'cp ' + backupdir + 'sudoers /etc/',
            'cp ' + backupdir + 'pkggetsudoers /usr/pkg/etc/',
            'cp ' + backupdir + 'prodeng.conf /etc/',
            
            'cp ' + backupdir + 'profile /etc/',
            'cp -r ' + backupdir + 'profile.d /etc/', 
            'cp ' + backupdir + 'ssh/ssh_host* /etc/',
            '(cp -r ' + backupdir + 'named /var/ && ln -s /var/named/named.conf /etc/named.conf)',
          
            'cp '+ backupdir + 'bps.sh /; chmod +x /bps.sh',
            '(cd ' + backupdir + 'yp; find . -depth -print | cpio -pdumv /var/yp/)',
        
            'cp /kernel/drv/sd.conf /var/tmp/sd.conf.orig',
            'cp /kernel/drv/ixgbe.conf /var/tmp/ixgbe.conf.orig',
            'cp ' + backupdir + 'sd.conf /kernel/drv/',
            'cp ' + backupdir + 'ixgbe.conf /kernel.drv/',
        
            
            'cp ' + backupdir + 'etc/ntp.keys /etc/ntp.keys /etc/' 
            'cp ' + backupdir + 'ntpdir/etc/inet/* /etc/inet',
            
            'mkdir /etc/ntp;cp ' + backupdir + 'ntpdir/etc/ntp/* /etc/ntp',
            
        
            ]
def backuphost():
    for cmd in cmd_list_backup:
        exec_command(cmd)

def restorehost():
    for cmd in cmd_list_restore:
        exec_command(cmd)
    
    
def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -B  to backup before OS Reinstall "
    print os.path.basename(sys.argv[0]) + " -R  to restore from backup after OS reinstall"
  
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "BRh")
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
                if o == "-h":
                        usage()
                        sys.exit(0)

                elif o == "-B":
                    backuphost()

                elif o == "-R":
                    restorehost();

if __name__ == "__main__":
        main()  

