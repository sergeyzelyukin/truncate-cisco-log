#!/usr/bin/python

import sys,os,datetime
from LogLine import LogLine

def recur():


def main():
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
  
  with open(log_filename, "rb") as source:
    pos = source_filesize/2
    source.seek(pos, 1)
    line = source.readline().strip()
    logline = LogLine(line)
    while not logline.ok:
      line = source.readline().strip()
      logline = LogLine(line)
    if logline.datetime.date() == target_date:
      print line
    elif logline.datetime.date() > target_date:
      print line
      source.seek(-pos/2, 1)
      line = source.readline().strip()
      logline = LogLine(line)
      while not logline.ok:
        line = source.readline().strip()
        logline = LogLine(line)
      print line
    else:
      print line
      source.seek(pos/2, 1)
      line = source.readline().strip()
      logline = LogLine(line)
      while not logline.ok:
        line = source.readline().strip()
        logline = LogLine(line)
      print line

if __name__ == "__main__":
  main()
  