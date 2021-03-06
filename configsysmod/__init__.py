#!/usr/bin/python
import paramiko,getopt,sys,copy,os,time,socket
##from pyssh import PySSH

rootdir='/var/tmp/collect2'
conf=rootdir + '/config/'
tmp=rootdir + '/tmp/'
stdoutcp=''
stderrcp=''
stdouttcplist=[]
sshhanddle=''
procmonsvr = 'procmonz1'
 

remote_path='/etc/resolv.conf'
local_path='/var/tmp/collect/config/resolve.conf'
#Transfering files to and from the remote machine

####AAAhostname='localhost'

def ssh_connect(hostname,user='',passwd=''):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		if not  passwd:
		        print "try to connect"	
       			#ssh.connect('localhost', username='root', password='abc123')
       			ssh.connect(hostname, username='root', password='abc123', timeout=10)
			return ssh
		else:
       			ssh.connect(hostname, username=user, password=passwd)
			return ssh
			
	#except paramiko.SSHException:
        except socket.error, e:
  	      print "Socket connection failed ", e
	      quit()

	except paramiko.SSHException, e:
              print "Connection Failed",e
              quit()

def read_stdout_err_in(stdout,stderr,stdin):
      	#print "sending stdin "
 	global stdoutcp,stderrcp
	global stdouttcplist
	#stdin.flush() 
      	print " reading stdout and stderr "
        for line in stdout.readlines():
	       	stdoutcp=line.strip()		
		stdouttcplist=stdouttcplist + [line.strip()]
         	print line.strip()
	for line in stderr.readlines():
		stderrcp=line.strip()
        	print line.strip()
	#for line in stdin.readlines():
        #	print line.strip()

def exec_cmd(hostname,cmd,user='',pwd=''):
	print "executing " + cmd
	ssh=ssh_connect(hostname,user,pwd)
	if ssh:
        	stdin,stdout,stderr = ssh.exec_command(cmd)
        	read_stdout_err_in(stdout,stderr,stdin)
		return ssh

def ldapclient_init(hostname):
        cmd="/usr/sbin/ldapclient init -v -a profileName=default -a domainName=tdn.hzl.ilx.com -a proxyDN=cn=proxyagent,ou=profile,dc=tdn,dc=hzl,dc=ilx,dc=com -a proxyPassword=\"proxyauth\" -a enableShadowUpdate=FALSE ldapz1.out.z1.tdn.hzl.ilx.com:389"
        exec_cmd(hostname,cmd)
	print("copying file of ldapz1 /var/ldap/cert8.db");
	remote_path='/var/ldap/cert8.db'
        local_path=conf+'confcert8.db'
    	put_get_file(local_path,remote_path,True,hostname)

	print("copying file of ldapz1 /var/ldap/key3.db ");
	remote_path='/var/ldap/key3.db'
        local_path=conf+'confkey3.db'
    	put_get_file(local_path,remote_path,True,hostname)

        
	print("copying file of ldapz1 /var/ldap/secmod.db ");
	remote_path='/var/ldap/secmod.db'
        local_path=conf+'confsecmod.db'
    	put_get_file(local_path,remote_path,True,hostname)
        

def put_get_file(local_path,remote_path,put,hostname):
	print "in put_get_file "
	ssh=ssh_connect(hostname)
	sftp = ssh.open_sftp()
        if put is True:
	        print "in put file "
		sftp.put(local_path, remote_path)
		sftp.close()
		ssh.close()
	else:
		sftp.get(remote_path, local_path)
		sftp.close()

		ssh.close()

def put_resolv(filename,hostname):
	print("Putting resolv.conf");
	remote_path='/etc/resolv.conf'
        local_path=conf+filename
    	put_get_file(local_path,remote_path,True,hostname)

def get_resolv(filename,hostname):
	print("getting resolv.conf");
	remote_path='/etc/resolv.conf'
        local_path=tmp+filename
	print " local path is :"+ local_path
    	put_get_file(local_path,remote_path,False,hostname)


def put_nsswitch(filename,hostname):
	print("Putting nsswitch.conf");
	remote_path='/etc/nsswitch.conf'
        local_path=conf+filename
    	put_get_file(local_path,remote_path,True,hostname)

def get_nsswitch(filename,hostname):
	print("getting nsswitch.conf");
	remote_path='/etc/nsswitch.conf'
        local_path=tmp+filename
	print " local path is :"+ local_path
    	put_get_file(local_path,remote_path,False,hostname)


def read_conf_file(filename,hostname):
        cmd='cat '+filename
      	print " reading the conf" + filename
        ssh=ssh_connect(hostname)
	stdin,stdout,stderr = ssh.exec_command(cmd)
        read_stdout_err_in(stdout,stderr)
	ssh.close()

def put_namedfiles(hostname):
	print "generate named.local"
        print "create directory /var/named" 
        exec_cmd(hostname,'mkdir /var/named')
	conffiler=conf+'confnamedlocal'
	conffilew=conf+'confnamedlocal.'+hostname

        with open(conffilew, "w") as fout:
		with open(conffiler, "r") as fin:
        		for line in fin:
            			fout.write(line.replace('template', hostname))

	print("Putting named.local");
	remote_path='/var/named/named.local'
        local_path=conffilew
    	put_get_file(local_path,remote_path,True,hostname)
        local_path=conf+'confnamedca'
        remote_path='/var/named/named.ca'
    	put_get_file(local_path,remote_path,True,hostname)
        local_path=conf+'confnamedconf'
        remote_path='/var/named/named.conf'
    	put_get_file(local_path,remote_path,True,hostname)
        exec_cmd(hostname,'ln -s /var/named/named.conf /etc/named.conf')


def put_zephyr(hostname,flag):
	print "putting zephyr file to " + hostname+' '+ str(flag)
	if str(flag) == '12':
		print("Putting zephyr.servers");
		remote_path='/etc/zephyr.servers'
        	local_path=conf + 'confzephyr-server12'
    		put_get_file(local_path,remote_path,True,hostname)
	elif str(flag) == '34':
		print("Putting zephyr.servers");
		remote_path='/etc/zephyr.servers'
        	local_path=conf + 'confzephyr-server34'
    		put_get_file(local_path,remote_path,True,hostname)


def put_ntpfiles(hostname):
	print "putting ntp files to " + hostname
	remote_path='/etc/inet/ntp.keys'
        local_path=conf + 'confntpkeys'
    	put_get_file(local_path,remote_path,True,hostname)
	remote_path='/etc/inet/ntp.client'
        local_path=conf + 'confntpclient'
    	put_get_file(local_path,remote_path,True,hostname)
	remote_path='/etc/inet/ntp.conf'
        local_path=conf + 'confntpconf'
    	put_get_file(local_path,remote_path,True,hostname)
	remote_path='/etc/inet/ntp.server'
        local_path=conf + 'confntpserver'
    	put_get_file(local_path,remote_path,True,hostname)
	remote_path='/etc/inet/ntp.drift'
        local_path=conf + 'confntpdrift'
    	put_get_file(local_path,remote_path,True,hostname)
        print "enable ntp service " 
	exec_cmd(hostname,'svcadm enable svc:/network/ntp:default')

def disable_someservices(hostname):
        print "disable svc:/network/routing/route"
	exec_cmd(hostname,'svcadm disable svc:/network/routing/route')
	print "disable  svc:/network/nis/server"
	exec_cmd(hostname,'svcadm disable svc:/network/nis/server')
	print "disable  svc:/network/nis/client"
	exec_cmd(hostname,'svcadm disable svc:/network/nis/client')
	print "disable  svc:/network/nis/xfr"
	exec_cmd(hostname,'svcadm disable svc:/network/nis/xfr')
	print "disable svc:/network/nis/passwd"
	exec_cmd(hostname,'svcadm disable svc:/network/nis/passwd')
	print "disable svc:/network/nis/update"
	exec_cmd(hostname,'svcadm disable svc:/network/nis/update')


def import_ns_and_autofs(hostname):
        print "importing name-service nscfg import"
	exec_cmd(hostname,'nscfg import -f name-service/switch')
	exec_cmd(hostname,'svcadm restart name-service/switch')
	print "configure mapid"
        exec_cmd(hostname,'sharectl set -p nfsmapid_domain=tdn.hzl.ilx.com nfs')
	print "importing dns/clent" 
        exec_cmd(hostname,'nscfg import -f dns/client')
	print "configuring nfs"
	exec_cmd(hostname,'svcadm enable svc:/network/nfs/status:default svc:/network/nfs/nlockmgr:default svc:/network/nfs/mapid:default svc:/network/nfs/client:default svc:/network/nfs/rquota:default')
	print "restarting autofs"
	exec_cmd(hostname,'svcadm restart autofs')
        print " executing sharectl nfsmapid "		 	
	exec_cmd(hostname,'sharectl set -p nfsmapid_domain=tdn.hzl.ilx.com nfs')


def imp_ldap_sudo(hostname):
        print "implementing LDAP sudo"
	print "removing tf_sudo-1.6.1.1"
	exec_cmd(hostname,'/usr/pkg/sbin/pkg_delete tf-sudo-1.6.1.1')
	print "Adding package sudo-1.8.15"
	exec_cmd(hostname,'/usr/pkg/sbin/pkg_add /packages/solaris-11.3-i86pc/sudo-1.8.15.tgz')
	print "Deleting /usr/bin/sudo"
	exec_cmd(hostname,'rm -f /usr/bin/sudo')
	print "creating softlink /usr/pkg/bin/sudo to /usr/bin/sudo"
        exec_cmd(hostname,'ln -s /usr/pkg/bin/sudo /usr/bin/sudo')
	print "renaming /usr/pkg/etc/sudoers to /usr/pkg/etc/sudoers.orig"
        exec_cmd(hostname,'mv /usr/pkg/etc/sudoers /usr/pkg/etc/sudoers.orig')
	print "creating softlink /etc/sudoers to /usr/pkg/etc/sudoers"
        exec_cmd(hostname,'ln -s /etc/sudoers /usr/pkg/etc/sudoers')
	print "copying /usr/pkg/etc/ldap.conf"
	remote_path='/usr/pkg/etc/ldap.conf'
        local_path=conf + 'confldap-conf'
    	put_get_file(local_path,remote_path,True,hostname)
	print "copying /etc/nsswitcht and import it into name-service/switch and refresh it"
	remote_path='/etc/nsswitch.conf'
        local_path=conf + 'confnsswitch-sudo-ldap'
    	put_get_file(local_path,remote_path,True,hostname)
        exec_cmd(hostname,'nscfg import -f name-service/switch')
        exec_cmd(hostname,'svcadm refresh name-service/switch')

def replace_procmon_SMF(hostname):
	print "svcadm disable ilx/procmon and svccfg delete ilx/procmon"
	exec_cmd(hostname,'svcadm disable ilx/procmon')
	exec_cmd(hostname,'svccfg  delete -f ilx/procmon')
 	print "copying S94local to /etc/rc2.d"		
	remote_path='/etc/rc2.d/S94local'
        local_path=conf + 'confS94local'
    	put_get_file(local_path,remote_path,True,hostname)
	global stdoutcp
	stdoutcp=0
        exec_cmd(hostname,'cat /var/spool/cron/crontabs/techsup|grep procmon|grep -v ^#|wc -l') 	
	if stdoutcp.strip() == '0':
        	exec_cmd(hostname,"echo '7,22,37,52 * * * * /ilx/procmon/sbin/up_procmon >/dev/null 2>&1' >> /var/spool/cron/crontabs/techsup") 	
		
	else:
        	print "\n\nprocmon startup crontab already exists !!!\n\n"	
	print "bounce procmon"
	exec_cmd(hostname,'/ilx/procmon/sbin/bounce_procmon')
	print "Check below updated crontab job of techsup user"
	exec_cmd(hostname,'cat /var/spool/cron/crontabs/techsup')

def create_hostfile(hostname):
        global stdouttcplist,stderrcp 	
	stderrcp=''
        print "creating and linking sysadmin/host and sysadmin/service"	
	exec_cmd(hostname,'ls /etc/sysadmin')	
	if 'No such ' in stderrcp:
		exec_cmd(hostname,'mkdir /etc/sysadmin;mv /etc/inet/hosts /etc/inet/services /etc/sysadmin/;ln -s /etc/sysadmin/hosts /etc/inet/hosts;ln -s /etc/sysadmin/services /etc/inet/services')
	else:
		print " /etc/sysadmins exist , symbolic link is not created !!"

       	print "creating hostfile entries"	
       	commandtorun=rootdir + '/checkhost3 -L' + hostname	
	#print "command tor un " + commandtorun
	stdouttcplist = []
	exec_cmd('localhost',commandtorun)
	if len(stdouttcplist) == 5:
		stdouttcplist = []
       	 	commandtorun=rootdir + '/checkhost3 -Q' + hostname	
		exec_cmd('localhost',commandtorun)
	if len(stdouttcplist) == 5:
		print "Server name is not on the master sheet!!!"
		return	
		print "len list" + str(len(stdouttcplist))
        buildhostfile()		
	remote_path='/etc/sysadmin/hosts'
        local_path=tmp + 'hostfile'
    	put_get_file(local_path,remote_path,True,hostname)

def buildhostfile():
        global stdouttcplist 	
    	fh=open(tmp + 'hostfile', 'w')
    	fr=open(conf + 'confhostinit', 'r')
        for line in fr:	
		fh.write(line)
        for line in stdouttcplist: 	
	        if 'Open' not in line:	
			fh.write(line+'\n')

def set_timezone(hostname,tzone):
  	print "set time zone to " + tzone
        exec_cmd(hostname,"svccfg -s svc:/system/timezone:default setprop timezone/localtime= astring: "+tzone)
	exec_cmd(hostname,"svcadm refresh svc:/system/timezone:default")
	print "Current time zone now "
	exec_cmd(hostname,"svccfg -s svc:/system/timezone:default listprop timezone/localtime") 	
	print "svcadm disable system/timezone "
	exec_cmd(hostname,"svcadm disable system/timezone") 	
	print "svcadm enable system/timezone "
	exec_cmd(hostname,"svcadm enable system/timezone") 	

def install_monet(hostname):
	print "sending the monet file to " + hostname 
	remote_path='/var/tmp/Monet.6.112.1.solaris10.ultra3.run'
        local_path=tmp + 'Monet.6.112.1.solaris10.ultra3.run'
    	put_get_file(local_path,remote_path,True,hostname)
	print "Installing monet now on " + hostname 
	exec_cmd(hostname,'cd /var/tmp;./Monet.6.112.1.solaris10.ultra3.run')




         
def install_procmon(hostname):
	global sshhandle,procmonsvr
	print "checking if procmon ssh key exist on " + hostname 
        username = 'indrah'
        password = 'h0gKRmqU'
    	ssh = PySSH()
    	ssh.connect(hostname,username,password)
    	output=ssh.runcmd('date')
    	print output
    	output=ssh.runcmd("su - techsup -c 'ssh marketz2 hostname'",True)
    	#output=ssh.runcmd("su - techsup -c 'hostname'",True)
    	print output.strip()
    	ssh.disconnect()

def ssh_keepalive(hostname):
        print "checking existing /etc/ssh/sshd_config"
        global stdoutcp
        stdoutcp=''
        exec_cmd(hostname,"cat /etc/ssh/sshd_config|grep 'ClientAliveInterval' |grep -v '^#' | wc -l")
        if stdoutcp.strip() == '0':
                exec_cmd(hostname,"echo ClientAliveInterval 60 >> /etc/ssh/sshd_config")
        print "restarting ssh daemon "	
        exec_cmd(hostname,"svcadm restart svc:/network/ssh")
	time.sleep(3)
	print "validate the sshd_config and testing if ssh works"
        exec_cmd(hostname,"cat /etc/ssh/sshd_config|egrep -i '(permitroot|clientaliveinterval)'")

def usage():
	print "\n -h for help "
	print " -R hostname  -t web,prod,hyper,tc -> update resolv.conf with  type of web,prod,host,ext " 
	print " -N hostname -> to update nsswitch.conf"
	print " -L hostname -> to configure local DNS"
        print " -D hostname -> to configure ldapclient" 
        print " -Z hostname,nn -> to update zephyr.server ( ie. -Z birdiez2,12 fo zephyrz1/2 and -Z birdiez2,34 for zephyrz3/4" 
  	print " -X hostname -x 'command to execute' ( ie. -X marketz2 -x 'ipadm' "
	print " -P hostname  -> to update ntp files"
        print " -S hostname -> disable some services"
        print " -A hostname -> import name service, nfs and autofs"
	print " -O hostname -> implement LDAP sudo"
	print " -C hostname -> remove SMF procmon, copy start up script and update crontab of techsup"
        print " -H hostname -> hostfile and service file link to /etc/sysadmin/ directory "		
        print " -Y hostname -y GMT0, EST5EDT, US/Eastern -> set server time zone "		
        print " -M hostname -> Install Monet"		
        print " -G hostname -> Install Procmon"		
	print " -K hostname -> configure ssh ClientAliveInterval"

def main():
    execflag=False
    resolv=False
    host=None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hR:r:N:n:L:D:Z:X:x:P:S:t:A:O:C:H:Y:y:M:G:K:")
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
		
    for o, a in opts:
		if o == "-h":
			usage()
			sys.exit(0)
		elif o == "-R": 
			resolv=True
		        host=a	
		elif o == "-t": 
			if resolv:
				if a == 'prod':
					put_resolv('confresolvprod',host)
				elif a == 'hyper':
					put_resolv('confresolvhyper',host)
				elif a == 'web':
					put_resolv('confresolvweb',host)
				elif a == 'host':
					put_resolv('confresolvhost',host)
				elif a == 'ext':
					put_resolv('confresolvext',host)
				elif a == 'webhost':
					put_resolv('confresolvwebhost',host)

		elif o == "-r": 
			get_resolv('confresolv',a)
		elif o == "-N":
			put_nsswitch('confnsswitch',a)
		elif o == "-n":
			get_nsswitch('confnsswitch',a)
		elif o == "-L":
			put_namedfiles(a)
		elif o == "-D":
			ldapclient_init(a)
		elif o == "-Z":
	                if a.endswith(',12'):     			
				a=a.replace(',12','')
				put_zephyr(a,12)
	                elif a.endswith(',34'):					
				
				a=a.replace(',34','')
				put_zephyr(a,34)
		elif o == "-X":
                        execflag=True
			exechost=a
                elif o == "-x":
			if execflag:
				exec_cmd(exechost,a)
                elif o == "-P":
			put_ntpfiles(a)

                elif o == "-S":
			disable_someservices(a)

                elif o == "-O":
			imp_ldap_sudo(a)

                elif o == "-A":
		  	import_ns_and_autofs(a)	

                elif o == "-C":
		  	replace_procmon_SMF(a)	

                elif o == "-H":
		  	create_hostfile(a)	

		elif o == "-Y":
                        execflag=True
			exechost=a

                elif o == "-y":
			print " in -z"
			if execflag:
				print "x in -z"
				set_timezone(exechost,a)
                elif o == "-M":
		  	install_monet(a)	

                elif o == "-G":
		  	install_procmon(a)	

                elif o == "-K":
		  	ssh_keepalive(a)	
		else:
			usage()
			assert False, "unhandled option"
		 
        #else:
        #    assert False, "unhandled option"



if __name__ == "__main__":
	main()


