#!/bin/env python

import subprocess,os,getopt,sys

dscript='./TraceFileDel.d'

def parse_file(file_dir):
        i=1
        if not os.path.lexists(file_dir):
                print "file or directory {} does not exist".format(file_dir)
                return False

        if os.path.isdir(file_dir):
                print "!!!!!!!"
                print "directory : {} will be monitored for deletion ".format(file_dir)
                print "!!!!!!!"

                ''' to resolve an issue if /usr/pkg64/ instead of /usr/pkg as argument '''

                blist=file_dir.split('/')
                while i < len(blist)-1:
                        if blist[len(blist)-i]:
                                bname=blist[len(blist) - i]
                                break
                        i+=1

                return bname
        elif os.path.isfile(file_dir):
                print "!!!!!!!"
                print "file : {} will be monitored for deletion ".format(file_dir)
                print "!!!!!!!"
                return os.path.basename(file_dir)
        else:
                print "file type is not supported"
                return False


def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -f full path of file name or directory name "

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:h")
    except getopt.GetoptError as err:
        print str(err)
        usage()
    for o, a in opts:
                if o == "-h":
                        usage()
                        sys.exit(0)
                elif o == "-f":
                    bname=parse_file(a)
                    if bname:
                        print "basename used by dtrace : " + bname
                        command = dscript + ' '+ bname
                        os.system(command)

if __name__ == "__main__":
        main()

