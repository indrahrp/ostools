
#! /usr/sbin/dtrace  -s

/* How to run the script:

./TraceFileDel.d 'the Basename of Filename to trace of which process delete it'

i.e
To trace of what process deleting  /usr/pkg64
./TraceFileDel.d pkg64

*/

#pragma D option quiet
int parentid ;

BEGIN
{
        parentid=-1;
        printf("Tracing file or folder : %s ... \n",$$1)

}


syscall::unlinkat:entry
/basename(copyinstr(arg1)) == $$1/
{
/* printing process which delete the file */

        printf("File/Folder %s has been deleted by :\nexecname : %s \npid %d \nppid %d\nuid %d \non %Y  \n", $$1, execname, pid,ppid,uid,walltimestamp);
        printf("Printing User Stack ");
        ustack();
        parentid = ppid ;
}

syscall:::entry
/pid == parentid/
{
/* printing parent process of process which delete the file */

        printf("execname of parent process : %s \n",execname);
        parentid = -1
}


