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
        
cmd_list_backup=['cp /etc/hosts ' + backupdir,
          'cp /etc/services ' + backupdir,
           'netstat -ni > ' + backupdir + 'netstatni.txt'
           'ipadm > ' + backupdir + 'ipadm.txt']
cmd_list_restore=['mkdir /etc/sysadmin && (mv /etc/inet/hosts /etc/inet/services /etc/sysadmin/;ln -s /etc/sysadmin/hosts /etc/inet/hosts;ln -s /etc/sysadmin/services /etc/inet/services)',
                 'cp /etc/ntp.keys /etc/' ]

for cmd in cmd_list:
    exec_command(cmd)


