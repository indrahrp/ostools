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
        
cmd_list=['cp /etc/hosts ' + backupdir,
          'cp /etc/services ' + backupdir,
           'netstat -ni > ' + backupdir + 'netstatni.txt'
           'ipadm > ' + backupdir + 'ipadm.txt']
for cmd in cmd_list:
    exec_command(cmd)


