#!/usr/bin/env python
#

import sys
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/Current/Extras/lib/python/PyObjC')
from Foundation import *
from datetime import datetime, timedelta
import subprocess

def main():
  # First get the OS X reported uptime (this is actual uptime as far as I understand it, excluding sleep)
  uptime_s = timedelta(seconds=int(NSProcessInfo.processInfo().systemUptime()))
  print 'uptime_osx_minutes:'+str(uptime_s.seconds/60),

  # Then get the Unix uptime, this is the total calendar time since last boot
  p = subprocess.Popen("uptime".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()
  if 'days' in stdout:
    uptime_days = stdout.split()[2]
    uptime_hours, uptime_minutes = stdout.split()[4][:-1].split(":")
  else:
    uptime_days = 0
    uptime_hours, uptime_minutes = stdout.split()[2][:-1].split(":")
  uptime = timedelta(days=int(uptime_days), hours=int(uptime_hours), minutes=int(uptime_minutes))
  print 'uptime_unix_minutes:'+str(int(uptime.total_seconds())/60)

if __name__ == '__main__':
  main()
