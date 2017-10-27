#!/usr/bin/env python

"""generic script for creating  zfs snapshot

v 1.0.0  
parameter:
	-h help
        -S zfs volume name
        -Number of Snapshot to Keep  	

ZfsSnap.py -h for help
ZfsSnap.py -S zfs volume  -D number of snapshot to keep

For example:

- to keep 4 snapshot: 
ZfsSnap -S home/packages -D 4

- to keep delete all snapshot: 

ZfsSnap -S zfs volume -D 0  

"""

import getopt,sys,os,re
import subprocess,re,pprint,csv,time,datetime




def snap_suffix(zfsvol):
    """generate snapshot suffix name with this format zfsvolname@YYYY_M_D_H_M_S (i.e rpool/zones@2017_9_22_19_25_11) """
    tm=time.localtime()
    suffix=str(tm.tm_year) +'_' + str(tm.tm_mon) + '_' +  str(tm.tm_mday) + '_' + str(tm.tm_hour) + '_'+  str(tm.tm_min) + '_' + str(tm.tm_sec)
    return suffix


def del_old_snapshot(zfsvol,keep):
    """ to delete old snapshot and keep the number of snapshot as requested """
    dictsnap={}
    listsnap=[]
    listdt=[]
    ret=True
    dkeys_todelete=[]
    print "\nChecking existing snapshot of " + zfsvol + ' ...'
    command = 'zfs list -rt snapshot ' + zfsvol
    lines=exec_command(command)

    snaplist=[ snap.split('@') for snap in lines[0].split() if zfsvol + '@' in snap ] 



    """ checking for snapshot with this name format i.e : rpool/zones@2017_9_22_19_25_11 """
    for snap,snapdt in snaplist:
	match = re.search(r'\d+_\d+_\d+_\d+_\d+_\d+', snapdt)
	if match:
                
		(year,month,day,hour,min,sec)=snapdt.split('_')
		conv_snapdt = datetime.datetime(int(year),int(month),int(day),int(hour),int(min),int(sec))
		dictsnap[conv_snapdt]=[snap,snapdt]
                 
    """ sort so the oldest one on first element on the list """
    dkeys=sorted(dictsnap)

    """ if snapshot to keep argument (-D arg) is greater than the number of existing snapshot """
    if int(keep) > len(dkeys):
	print '\n!!! No snapshot to be deleted, the number of snapshot of ' + zfsvol + ' is under ' + keep
	return  True

    """ if -D 0 """
    if int(keep) == 0:
        keep=1 
	ret=False

    """ create another list for the snapshot to be deleted """
    for key in range(0,(len(dkeys) - (int(keep)-1))):
	dkeys_todelete.append(dkeys[key])

    """ delete the snapshot """
    for key in dkeys_todelete:
	snap_to_delete=str(dictsnap[key][0])+'@'+str(dictsnap[key][1])
	print "\nDeleting old snapshot " +  snap_to_delete +' ...'
	command='zfs destroy ' + snap_to_delete
        lines=exec_command(command)

    """ if error send email  """ 
    if lines[1]:
        	subject='delete snapshot ' + snapname +'  is failed'
		esubject=""" " """ + subject + """ " """
                send_email(esubject)
    return ret    
    
def exec_command(command):

	""" to call OS command from python """
        print "==> executing command :  " + command        
        active_link=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines=active_link.communicate()
        print "Output : " + lines[0]
        print "Error : " + lines[1]
        return lines
        

def create_snapshot(zfsvol,suffix):
        """ to create snapshot with name formatted as zfsvolname@YYYY_M_D_H_M_S (i.e rpool/zones@2017_9_22_19_25_11)   """

	snapname=zfsvol+'@'+suffix
	print "\nCreating snapshot " +  snapname + ' ...'
	command='zfs snapshot ' + snapname
	lines=exec_command(command)
        """ If error send  email """	
	if lines[1]:
		subject='create snapshot ' + snapname +' is failed '  
                esubject=""" " """ + subject + """ " """
		send_email(esubject)
	print "\n"


def send_email(subject):
        """ send email for any job failure """	

    	command='mailx  -s ' + subject + '  indra.harahap@thomsonreuters.com < /dev/null '
    	print "command  " + command
    	exec_command(command)  
        
          
def usage():

    """ for print help """
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -S zfs volume  -D number of snapshot to keep"
    print "For example : " + os.path.basename(sys.argv[0]) + " -S home/packages -D 4 "
    
    
def main():
    """ main """
    zfsvol=None
    keep=None
    opts=None
    args=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "S:D:h")
    except getopt.GetoptError as err:
        print str(err)
        usage()
	sys.exit(0)
              
    for o,a in opts:
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

    if zfsvol and keep:                
        suffix=snap_suffix(zfsvol)
        flag=del_old_snapshot(zfsvol,keep)
	if flag:
        	create_snapshot(zfsvol,suffix)	
	else:
		print "!!! No new snapshot created "
        
    
    

if __name__ == "__main__":
        main()  

