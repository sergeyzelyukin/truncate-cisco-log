#!/usr/bin/python

import sys,os,datetime
from LogLine import LogLine

class LogFile(file):
  INITIAL_OFFSET = 4096
  MAX_FAST_GROW = 512000
  INCREMENTAL_GROW = 256000
  
  def __init__(self, _filename):
    self._filename = _filename
    self._date = None
    self._logline = None
    self._line_pos = None
    super(LogFile,self).__init__(_filename, "rb")
    self._filesize = os.path.getsize(_filename)

  def fast_rewind(self):
    if not self._date:
      raise Exception("no date given") 
    
    if not self._filesize > 0:
      return False 

    # Start from the middle
    start_pos = self._filesize/2
    self.seek(start_pos, 0)    
    return self.recursive_jumps_to_date(start_pos)

  def read_until_logline(self):
    while True:
      line_pos = self.tell()
      line = self.readline()
      if not line:
        # EOF
        return False
      logline = LogLine(line)
      if logline.ok:
        # line is ok, save it
        self._line_pos = line_pos
        self._logline = logline
        return True

  def recursive_jumps_to_date(self, offset):
    if not self.read_until_logline():
      # No logline found
      return False
    
    if self._logline.datetime.date() == self._date:
      # Search completed
      return True
    else:
      new_offset = offset/2
      if new_offset == 0:
        # no place no jump
        return False

      new_offset = -new_offset if self._logline.datetime.date() > self._date else new_offset

      self.seek(new_offset, 1)
      if self.tell() == self._line_pos:
        # Already read from here
        return False

      return self.recursive_jumps_to_date(abs(new_offset))

  def back_rewind(self):
    offset = LogFile.INITIAL_OFFSET
    found = False
    while True:
      # offset from last ok line
      new_pos = self._line_pos-offset
      if new_pos<0:
        new_pos = 0
      self.seek(new_pos, 0)

      if not self.read_until_logline():
        # impossible
        raise Exception("unable to find line, even previously found")

      if self._logline.datetime.date()<self._date:
        # found prev date
        found = True
        break
      if new_pos == 0:
        # begin was already reached, stop
        break      
      if offset<LogFile.MAX_FAST_GROW:
        offset *= 2 # fast jumps
      else:
        offset += LogFile.INCREMENTAL_GROW # incremental jumps
    return found 

  def forward_rewind(self):
    while True:
      if not self.read_until_logline():
        # impossible
        raise Exception("unable to find line, even previously found")
      if self._logline.datetime.date()==self._date:
        # found
        return True
    
  @property
  def filename(self):
    return self._filename
    
  @property
  def logline(self):
    return self._logline
    
  @property
  def date(self):
    return self._date
    
  @date.setter
  def date(self, _date):
    self._date = _date



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
      
      
