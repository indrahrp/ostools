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
            
            'netstat -nr > ' + backupdir + 'netstatnr.txt',
            'zfs list > ' + backupdir + 'zfslist.txt',
            'zpool status > ' + backupdir + 'zpoolstatus.txt',
            'zpool list > + ' + backupdir + 'zpoollist.txt',
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
            
            
            "(cd /var/spool/cron/crontabs && for user in `ls -tlr | awk '{print $9}'|grep -v ^$`;do  echo 'USER ' $user >> ' + backupdir + 'cronbck ; cat $user >> ' + backupdir + 'cronbck;done)",


            
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
            'cp ' + backupdir + 'hosts /etc/sysadmin/hosts',
            'cp ' + backupdir + 'services /etc/sysadmin/services',
            'cp ' + backupdir + 'etc/ntp.keys /etc/ntp.keys /etc/' 
            ]
for cmd in cmd_list_backup:
    exec_command(cmd)

for cmd in cmd_list_restore:
    exec_command(cmd)
