#!/usr/bin/python

import sys,os,datetime
from LogFile import LogFile

# Get params
if not len(sys.argv)==4:
  print "usage: {0} <LOG FILENAME> <MONTH> <DAY>".format(sys.argv[0])
  sys.exit(1)
else:
  log_filename = sys.argv.pop(1)

if not os.path.exists(log_filename):
  print "there is no such file"
  sys.exit(1)
  
try:
  target_date = datetime.datetime.strptime('{0} {1} 2017'.format(sys.argv.pop(1), sys.argv.pop(1)), "%m %d %Y").date()
except:
  print "wrong date"
  sys.exit(1)

# Check
source_filesize = os.path.getsize(log_filename)
if source_filesize == 0:
  print "empty file"
  sys.exit(1)

# Searching
with LogFile(log_filename) as lf:
  lf.date = target_date
  if not lf.fast_rewind():
    print "date does not exist in file"
    sys.exit(1)

  if not lf.back_rewind():
    # last read date is the lowest
    print str(lf.logline.datetime)  

  if lf.forward_rewind():
    # found first occurence of date
    print str(lf.logline.datetime)
  else:
    # impossible
    raise Exception("cannot return to date")
      
      
