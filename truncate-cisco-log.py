#!/usr/bin/python

import sys,os,datetime
from LogLine import LogLine

def read_until_ok():
  while True:
    line_pos = fh.tell()
    line = fh.readline()
    if not line:
      #print "eof"
      return -1
    logline = LogLine(line)
    if logline.ok:
      break


def find_date(fh, offset):
  while True:
    line_pos = fh.tell()
    line = fh.readline()
    if not line:
      #print "eof"
      return -1
    logline = LogLine(line)
    if logline.ok:
      break
  #print line.strip()
  if logline.datetime.date() == target_date:
    #print "Search completed"
    return line_pos
  else:
    new_offset = offset/2
    if new_offset == 0:
      #print "not found"
      return -1
    new_offset = -new_offset if logline.datetime.date() > target_date else new_offset
    fh.seek(new_offset, 1)
    return find_date(fh, abs(new_offset))


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

source_filesize = os.path.getsize(log_filename)

if source_filesize == 0:
  print "empty file"
  sys.exit()

with open(log_filename, "rb") as source:
  start_pos = source_filesize/2
  source.seek(start_pos, 1)
  date_pos = find_date(source, start_pos)
  if date_pos<0:
    print "not found"
    sys.exit()
  source.seek(date_pos, 0)
  
