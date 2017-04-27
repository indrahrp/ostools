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
            'cd /usr/pkg; find . -depth -print | cpio -pdumv ' + backupdir + 'usr/pkg',   
            'cd /usr/local;find . -depth -print | cpio -pdumv ' + backupdir + 'usr/local',
            'cd /var/db;find . -depth -print | cpio -pdumv ' + backupdir + 'var/db',
            'cd /var/bbmon; find . -depth -print | cpio -pdumv ' + backupdir + 'var/bbmon',
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
            'ifconfig -a > ' + backupdir + 'ifconfiga'
            
            'cp /etc/hosts ' + backupdir,
            'cp /etc/services ' + backupdir,
            'netstat -ni > ' + backupdir + 'netstatni.txt',
            'ipadm > ' + backupdir + 'ipadm.txt']
cmd_list_restore=['mkdir /etc/sysadmin && (mv /etc/inet/hosts /etc/inet/services /etc/sysadmin/;ln -s /etc/sysadmin/hosts /etc/inet/hosts;ln -s /etc/sysadmin/services /etc/inet/services)',
                 'cp /etc/ntp.keys /etc/' ]

for cmd in cmd_list_backup:
    exec_command(cmd)


