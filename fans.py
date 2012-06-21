#!/usr/bin/env python
#

import sys
import subprocess
import re
import os

def getFanSpeeds(smc):
    fans = {}
    command = [smc, '-f']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    stdout = stdout.split('\n')
    for key,item in enumerate(stdout):
        if re.match('Fan', item):
            fan = item.replace(' #', '').lower()
            fans[fan] = stdout[key+1].split()[-1]
    return fans

def main():
    ## SETUP ##
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    smc = script_dir+'/smc'
    ## ----- ##
    fans = getFanSpeeds(smc)
    for fan in sorted( fans.keys(), key=lambda x: fans[x] ):
        print fan +""+ fans[fan],

if __name__ == '__main__':
    main()
