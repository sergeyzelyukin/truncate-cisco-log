#!/usr/bin/python

import sys,os,datetime,time
from LogFile import LogFile

def copy_logfile_till_end(source, dest_filename):
  return
  with open(dest_filename, "w") as dest:
    for line in source:
      dest.write(line)


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
start = time.time()
with LogFile(log_filename) as lf:
  lf.date = target_date
  if not lf.fast_rewind():
    stop = time.time()
    print "date does not exist in file (time spent: %.1f)"%(stop-start)
    sys.exit(1)

  if not lf.back_rewind():
    # last read date is the lowest
    stop = time.time()
    print "found: %s, time spent: %.1f"%(str(lf.logline.datetime), stop-start)

    start = time.time()
    trunc_filename = log_filename+".trunc"
    copy_logfile_till_end(lf, trunc_filename)
    stop = time.time()
    print "wrote: %s, time spent: %.1f"%(trunc_filename, stop-start)

  if lf.forward_rewind():
    # found first occurence of date
    stop = time.time()
    print "found: %s, time spent: %.1f"%(str(lf.logline.datetime), stop-start)

    start = time.time()
    trunc_filename = log_filename+".trunc"
    copy_logfile_till_end(lf, trunc_filename)
    stop = time.time()
    print "wrote: %s, time spent: %.1f"%(trunc_filename, stop-start)
  else:
    # impossible
    stop = time.time()
    raise Exception("cannot return to date (time spent: %.1f)"%(stop-start))
      
      
