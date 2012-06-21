#!/usr/bin/env python
#

import csv
import sys
import subprocess
import re
import os
from datetime import datetime

def getTempReadings(tempmonitor, all=True):
    sensors = {}
    command = [tempmonitor, '-l']
    if all: command.append('-a')
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout,stderr = proc.communicate()
    for line in stdout.split('\n')[:-1]:
        l = line.split()
        if len(l) == 4: sensors["_".join(l[1:2]).lower().strip(':')] = l[2]
        elif len(l) == 5: sensors["_".join(l[1:3]).lower().strip(':')] = l[3]
        elif len(l) == 6: sensors["_".join(l[1:4]).lower().strip(':')] = l[4]
        elif len(l) == 7: sensors["_".join(l[1:5]).lower().strip(':')] = l[5]
        elif len(l) == 8: sensors["_".join(l[1:6]).lower().strip(':')] = l[6]
        elif len(l) == 9: sensors["_".join(l[1:7]).lower().strip(':')] = l[7]
        elif len(l) == 10: sensors["_".join(l[1:8]).lower().strip(':')] = l[8]
        elif len(l) == 11: sensors["_".join(l[1:9]).lower().strip(':')] = l[9]
    return sensors

def main():
    ## SETUP ##
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    tempmonitor = script_dir+'/tempmonitor'
    ## ----- ##
    sensors = getTempReadings(tempmonitor)
    for sensor in sensors:
        print sensor+':'+sensors[sensor], 

if __name__ == '__main__':
    main()
