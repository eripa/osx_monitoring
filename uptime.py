#!/usr/bin/env python
#

from Foundation import *
from datetime import datetime, timedelta

def main():
    uptime_s = timedelta(seconds=int(NSProcessInfo.processInfo().systemUptime()))
    print 'uptime_minutes:'+str(uptime_s.seconds/60)
    
if __name__ == '__main__':
    main()
