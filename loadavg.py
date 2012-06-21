#!/usr/bin/env python
#

import subprocess

def getLoadAvg():
    loads = []
    command = ["uptime"]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    result = stdout.split('\n')[0].split()[-3:]
    loads.append('load1m:'+result[0])
    loads.append('load5m:'+result[1])
    loads.append('load15m:'+result[2])
    return loads

def main():
    loads = getLoadAvg()
    for load in loads:
        print load,
    
if __name__ == '__main__':
    main()
