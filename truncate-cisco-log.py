#!/usr/bin/python

import sys,os,datetime
from LogLine import LogLine

def read_until_logline(fh):
  while True:
    line_pos = fh.tell()
    line = fh.readline()
    if not line:
      # EOF
      return (-1, Null)
    logline = LogLine(line)
    if logline.ok:
      return (line_pos, logline)


def find_date(fh, offset):
  line_pos, logline = read_until_logline(fh)
  if line_pos<0:
    # No logline found
    return line_pos
    
  if logline.datetime.date() == target_date:
    # Search completed
    return line_pos
  else:
    new_offset = offset/2
    if new_offset == 0:
      # not found
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

  i = 1
  found = False
  while True:
    offset = date_pos-1024*i
    if offset<0:
      offset = 0
    source.seek(offset, 0)

    line_pos, logline = read_until_logline(source)
    if line_pos<0:
      print "strange situation"
      sys.exit()

    print "reading back..."
    print str(logline.datetime)

    if logline.datetime.date()<target_date:
      found = True
      print "found prev date..."
      break
    
    if offset == 0:
      print "begin reached..."
      break
      
    i+=1
  
  if not found:
    print "prev date not found..."
    print str(logline.datetime)  
  else:
    while True:
      line_pos, logline = read_until_logline(source)        
      if line_pos<0:
        print "strange situation"
        sys.exit()
      if logline.datetime.date()==target_date:
        print "found..."
        print str(logline.datetime)
        break
      
      
      
