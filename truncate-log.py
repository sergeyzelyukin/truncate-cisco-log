#!/usr/bin/python

import sys,os

def main():
  if not len(sys.argv)==2:
    print "usage: {0} <LOG FILENAME>".format(sys.argv[0])
    sys.exit(1)
  else:
    log_filename = sys.argv.pop()

  if not os.path.exists(log_filename):
    print "there is no such file"
    sys.exit(1)

  source_filesize = os.path.getsize(log_filename)
  

if __name__ == "__main__":
  main()
  