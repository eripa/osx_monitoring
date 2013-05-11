#!/usr/bin/env python
#
# Use this script to download and extract the dependency binaries
#

import urllib2
from bs4 import BeautifulSoup
import re
import mechanize
import hashlib
import shlex
import subprocess
import os
import shutil

class TempMonitor(object):
  """docstring for TempMonitor"""
  def __init__(self):
    self.url = 'http://www.bresink.de/osx/0TemperatureMonitor/download.php5'
    self.sha1 = self.getSHA1forTempMonitor(verbose=False)
    self.archive = "tempmonitor.dmg"

  def getSHA1forTempMonitor(self, verbose=False):
    sha1 = None
    download_url = None
    main_page = urllib2.urlopen(self.url)
    soup = BeautifulSoup(main_page.read())
    if verbose: print "Getting SHA1 for TempMonitor download..",
    # Extract the SHA1 for later verification
    for paragraph in soup.find_all('p'):
        sha1_regex = re.compile('.*([0-9a-f]{40}).*')
        match = sha1_regex.match(paragraph.getText())
        if match: sha1 = match.groups()[0]

    if sha1:
      if verbose: print 'Got: %s' % (sha1)
    else:
      if verbose: print "Couldn't find SHA1, will skip checksum verification"

    return sha1

  def download(self):
    br = mechanize.Browser()
    br.open(self.url)
    br.select_form(name="Download")
    response1 = br.submit()
    print "Downloading TempMonitor..."
    with open(self.archive, "w") as f:
      f.write(response1.read())
    if self.sha1:
      # let's verify sha1
      print "Verifying SHA1 checksum...",
      if self.sha1 == hashlib.sha1(open(self.archive, 'rb').read()).hexdigest():
        print "Success!"
      else:
        print "Failed, this might cause problems later on.."
    return self.archive

  def extract(self):
    # First convert the archive to be able to automatically mount it later
    convert_command = "hdiutil convert -quiet %s -format UDTO -o tempmonitor.cdr" % (self.archive)
    attach_command = "hdiutil attach -quiet -nobrowse -noverify -noautoopen -mountpoint tempmount tempmonitor.cdr"
    detach_command = "hdiutil detach -force -quiet tempmount"
    print 'Attaching image...',
    subprocess.call(shlex.split(convert_command))
    subprocess.call(shlex.split(attach_command))
    print 'Done!'
    # Copy the files that we need..
    print 'Copying tempmonitor binary and detaching image...',
    shutil.copy("tempmount/TemperatureMonitor.app/Contents/MacOS/tempmonitor", ".")
    subprocess.call(shlex.split(detach_command))
    print 'Done!'

  def clean(self):
    print "Cleaning archive...",
    basename = self.archive.split('.')[0]
    # remove both archives
    os.remove(basename+'.cdr')
    os.remove(basename+'.dmg')
    print "Done!"


def main():
  tempmonitor = TempMonitor()
  tempmonitor.download()
  tempmonitor.extract()
  tempmonitor.clean()


if __name__ == '__main__':
  main()