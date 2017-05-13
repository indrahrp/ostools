#!/bin/python

import getopt,sys,os,re
#from collections import OrderedDict 
import subprocess,re,pprint,csv

backupdir='/var/tmp/pkgbck/'

def exec_command(command):
        print "executing command :  " + command        
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
            'cp -p /etc/inet/static_routes-DefaultFixed  ' + backupdir + 'static_routes-DefaultFixed.txt',
            'cp -p /etc/system ' + backupdir + 'system',
            'cp -p /etc/rc2.d/S68ndd ' + backupdir,    
            'cp -p /etc/resolv.conf ' + backupdir,
            'cp -p /etc/nsswitch.conf ' + backupdir,
            'cp -p  /etc/zephyr.servers ' + backupdir,
            'ipadm > ' + backupdir + 'ipadm',
            'dladm show-link > ' + backupdir + 'dladmshowlinks',
            'dladm show-phys -L > ' + backupdir + 'dladmshowphysL',
            'dladm show-vnic > ' + backupdir + 'dladmshowvnic',
            'ifconfig -a > ' + backupdir + 'ifconfiga',
            'cp -p /etc/gateways ' + backupdir,
            'netstat -nr > ' + backupdir + 'netstatnr.txt',
            'zfs list > ' + backupdir + 'zfslist.txt',
            'zpool status > ' + backupdir + 'zpoolstatus.txt',
            'zpool list >  ' + backupdir + 'zpoollist.txt',
            'zfs get all > ' + backupdir + 'zfsgetall.txt',
            'zpool  get all gtplog > ' + 'zpoolgetallgtplog.txt',
            'zpool get all ilx > ' + 'zpoolgetallilx.txt',
            'zpool get all rpool > ' + 'zpoolgetallrpool.txt',
            'diskinfo   > ' + backupdir + 'diskinfo.txt',
            'date >  '+ backupdir + 'date.txt',
            'svccfg -s svc:/system/environment:init listprop environment/LANG > ' + backupdir + 'envlang.txt',
            'svccfg -s svc:/system/timezone:default listprop timezone/localtime > ' + backupdir + 'timezonelocaltime.txt',
            'svccfg -s system/environment:init listprop environment/TZ > ' + backupdir + 'environmentTZ.txt',
            'cp -p /etc/hosts ' + backupdir,
            'cp -p /etc/services ' + backupdir,   

            'cp -p /etc/vfstab ' + backupdir,
            'cp -p /etc/dfs/dfstab '+ backupdir,
            '(cd /var/spool/cron;cp -pr crontabs/ ' + backupdir +'crontabs)',
            'cp -p /etc/sudoers ' + backupdir + 'sudoers',
            'cp -p /usr/pkg/etc/sudoers ' + backupdir + 'pkgetcsudoers',
            'cp -p /etc/prodeng.conf ' + backupdir + 'prodeng.conf',
            'cp -p /etc/profile ' + backupdir  + 'profile',
            'cp -pr /etc/profile.d ' + backupdir + 'profile.d',
            
            
            'prtdiag -v > ' + backupdir + 'prtdiagv',
            'psrinfo > ' + backupdir + 'psrinfo',
            'cp -p /etc/passwd  ' + backupdir + 'passwd.txt',
            'cp -p /etc/shadow  ' + backupdir + 'shadow.txt',
            'cp -p /etc/group  ' + backupdir + 'group.txt',
            'cp -pr /etc/ssh ' + backupdir,
            'cp -pr /var/named ' + backupdir,
            'cp -pr /var/yp ' + backupdir, 
            'mkdir -p /var/tmp/pkgbck/kerneldrv/ ; cp -r /kernel/drv ' + backupdir + 'kerneldrv/',
            'cp -p /bps.sh ' + backupdir, 
            'cp -p /etc/inetd.conf ' + backupdir,
            'cp -p /etc/hosts ' + backupdir + 'hosts1',
            'cp -p /etc/services ' + backupdir + 'services1',
            'beadm list > ' + backupdir + 'beadmlist',
            
            
            "(cd /var/spool/cron/crontabs && for user in `ls -tlr | awk '{print $9}'|grep -v ^$`;do  echo 'USER ' $user >> " + backupdir + "cronbck ; cat $user >> " + backupdir + "cronbck;done)",


            
            'cp -p /kernel/drv/sd.conf ' + backupdir,
            'cp -p /kernel/drv/ixgbe.conf ' + backupdir,
            'cp -p /kernel/drv/nxge.conf ' + backupdir,
            'cp -p /kernel/drv/nge.conf ' + backupdir, 
            'cp -p /kernel/drv/nxge.conf ' + backupdir, 
            'cp -p /kernel/drv/igb.conf ' + backupdir, 
            'cp -p /kernel/drv/igbvf.conf ' + backupdir, 



            '(mkdir -p ' + backupdir + 'ntpdir/etc/inet ; mkdir -p ' + backupdir + 'ntpdir/etc/ntp/ ;cp -p /etc/inet/ntp* ' + backupdir + 'ntpdir/etc/inet;cp -p /etc/ntp/* ' + backupdir + 'ntpdir/etc/ntp/; cp -p /etc/ntp.keys  ' + backupdir + 'ntpdir/etc)',
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
            'cp -p /etc/inetd.conf ' + backupdir,
            'inetadm > ' + backupdir + 'inetadm.txt',
            
            
            'netstat -ni > ' + backupdir + 'netstatni.txt',
            'mkdir -p ' + backupdir + 'autosys',
            'mkdir -p ' + backupdir + 'usr/openwin/lib/app-defaults/',
            'mkdir -p ' + backupdir + 'usr/lib/X11/app-defaults',
            '(cd  /usr/openwin/lib/app-defaults/ && cp -p * ' + backupdir + 'usr/openwin/lib/app-defaults/)',
            '(cd usr/lib/X11/app-defaults && cp -p * ' + backupdir + 'usr/lib/X11/app-defaults/)',
            'cp -p /usr/lib/libsybdb* ' + backupdir + 'autosys/',
            
            
            '(mkdir -p ' + backupdir + 'etcdir ; cd /etc/ && find . -depth -print |cpio -pdumv ' + backupdir + 'etcdir)'
          
           ]



cmd_list_restore=[
            'mkdir /etc/sysadmin && (mv /etc/inet/hosts /etc/inet/services /etc/sysadmin/;ln -s /etc/sysadmin/hosts /etc/inet/hosts;ln -s /etc/sysadmin/services /etc/inet/services)',
            'cp -p ' + backupdir + 'system /etc/',
            '(cp -p ' + backupdir + 'S68ndd /etc/rc2.d && chmod +x /etc/rc2.d/S68ndd)',
            'cp -p ' + backupdir +'resolv.conf /etc/',
            'cp -p ' + backupdir  + 'nsswitch.conf /etc/',
            'cp -p ' + backupdir + 'zephyr.servers /etc/',
            'cp -p ' + backupdir + 'gateways /etc/',
            
            "cat " + backupdir + "envlang.txt | awk '{print $3}' | xargs svccfg -s svc:/system/environment:init setprop environment/LANG = astring:",
            "cat " + backupdir + "environmentTZ.txt |awk '{print $3}'| xargs  svccfg -s system/environment:init setprop environment/TZ=",
            'svcadm refresh svc:/system/timezone:default',
        
            'svcadm refresh svc:/system/environment:init',
            "cat " + backupdir + "timezonelocaltime.txt |awk '{print $3}'| xargs  svccfg -s svc:/system/timezone:default setprop timezone/localtime= astring:",
            'svcadm refresh svc:/system/timezone:default',
            
            'cp -p ' + backupdir + 'hosts /etc/sysadmin/hosts',
            'cp -p ' + backupdir + 'services /etc/sysadmin/services',
            
             "(cd " + backupdir + "crontabs;for user in `ls |egrep -vi '(root|sys|adm|lp|snmp)'`;do  cp -p $user /var/spool/cron/crontabs;done)",
            'cp -p ' + backupdir + 'sudoers /etc/',
            'cp -p ' + backupdir + 'pkggetsudoers /usr/pkg/etc/',
            'cp -p ' + backupdir + 'prodeng.conf /etc/',
            
            'cp -p ' + backupdir + 'profile /etc/',
            'cp -pr ' + backupdir + 'profile.d /etc/', 
            'cp -p ' + backupdir + 'ssh/ssh_host* /etc/ssh/',
            '(cp -pr ' + backupdir + 'named /var/ && ln -s /var/named/named.conf /etc/named.conf)',
          
            'cp -p ' + backupdir + 'bps.sh /; chmod +x /bps.sh',
            'cp -rp ' + backupdir + 'yp/* /var/yp/',
        
            'cp -p /kernel/drv/sd.conf /var/tmp/sd.conf.orig',
            'cp -p /kernel/drv/ixgbe.conf /var/tmp/ixgbe.conf.orig',
            'cp -p ' + backupdir + 'sd.conf /kernel/drv/',
            'cp -p ' + backupdir + 'ixgbe.conf /kernel/drv/',
        
            
            'cp -p ' + backupdir + 'etc/ntp.keys  /etc/',
            'cp -p ' + backupdir + 'ntpdir/etc/inet/* /etc/inet',
            
            'mkdir /etc/ntp;cp -p ' + backupdir + 'ntpdir/etc/ntp/* /etc/ntp',
            
        
            ]

cmd_list_rest=[
            'svcadm enable /network/dns/server',
            'nscfg import -f dns/client',
            'nscfg import -f name-service/switch',
            'svcadm enable ntp',
            'svccfg -s system/environment:init refresh',
            'svcadm restart system/environment:init',
            'zpool upgrade -a',
            'zfs upgrade -a'

    ]

cmd_list_nis=[
     
            'nscfg import -f /network/nis/domain; svcadm restart nis/domain',
            'svcadm enable  svc:/network/nis/domain:default',
            'svcadm enable /network/nis/client',
            'pkg install service/network/nis',
            'nscfg import -f /network/nis/domain; svcadm restart nis/domain',

            'svcadm disable svc:/network/nis/xfr:default',
            'svcadm disable svc:/network/nis/update:default',
            'svcadm disable svc:/network/nis/passwd:default',
            'svcadm disable svc:/network/nis/domain:default',
            'svcadm disable svc:/network/nis/client:default',
            'svcadm disable svc:/network/nis/server:default',

            'svcadm enable svc:/network/nis/xfr:default',
            'svcadm enable svc:/network/nis/update:default',
            'svcadm enable svc:/network/nis/passwd:default',
            'svcadm enable svc:/network/nis/domain:default',
            'svcadm enable svc:/network/nis/client:default',
            'svcadm enable svc:/network/nis/server:default',
            'nscfg import -f /network/nis/domain; svcadm restart nis/domain',
            "grep '^+' /etc/shadow || echo '+::::::::' >> /etc/shadow",
            "grep '^+' /etc/passwd || echo '+' >> /etc/passwd",


    
    ]

cmd_list_nfs=[
    
            'svcadm enable svc:/network/nfs/status:default svc:/network/nfs/nlockmgr:default svc:/network/nfs/mapid:default svc:/network/nfs/client:default svc:/network/nfs/rquota:default', 
            'svcadm restart autofs',
            'svcadm enable /system/name-service-cache'

    ]

cmd_list_rest_autosys=[
            '[ ! -f /usr/lib/libsybdb.so ] && cp -p ' + backupdir + 'autosys/libsybdb.so /usr/lib/'
            
            
        ]



def configure_nis(a):
    exec_command('echo '+ a + ' > /etc/defaultdomain')
    exec_command('domainname ' + a)
    for cmd in cmd_list_nis:
        exec_command(cmd)
    
def configure_nfs(a):
    exec_command('sharectl set -p nfsmapid_domain=' + a + ' nfs')
    for cmd in cmd_list_nfs:
        exec_command(cmd)



def backuphost():
    for cmd in cmd_list_backup:
        exec_command(cmd)

def restorehost():
    for cmd in cmd_list_restore:
        exec_command(cmd)
        
def restofcommand():
     for cmd in cmd_list_rest:
        exec_command(cmd)

def restoreautosys():
     for cmd in cmd_list_rest_autosys:
        exec_command(cmd)
    
    
def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -B  to backup before OS Reinstall "
    print os.path.basename(sys.argv[0]) + " -R  to restore from backup after OS reinstall"
    print os.path.basename(sys.argv[0]) + " -L  to run rest of command after OS reinstall"
    print os.path.basename(sys.argv[0]) + " -N 'domain name' - to configure NIS after OS reinstall"
    print os.path.basename(sys.argv[0]) + " -F 'domain name' - to configure NFS after OS reinstall"
    print os.path.basename(sys.argv[0]) + " -A to restore autosys files after OS reinstall"
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "BRLN:F:Ah")
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
                elif o == "-L":
                    restofcommand();
                elif o == "-N":
                    configure_nis(a);
                elif o == "-F":
                    configure_nfs(a);
                elif o == "-A":
                    restoreautosys();
                
                

if __name__ == "__main__":
        main()  

