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

def getSHA1forTempmonitor(url):
  sha1 = None
  download_url = None
  main_page = urllib2.urlopen(url)
  soup = BeautifulSoup(main_page.read())
  print "Getting SHA1 for TempMonitor download..",
  # Extract the SHA1 for later verification
  for paragraph in soup.find_all('p'):
      sha1_regex = re.compile('.*([0-9a-f]{40}).*')
      match = sha1_regex.match(paragraph.getText())
      if match: sha1 = match.groups()[0]

  if sha1:
    print 'Got: %s' % (sha1)
  else:
    print "Couldn't find SHA1, will skip checksum verification"

  return sha1

def downloadTempMonitor(url, sha1=None):
  tempmon_archive = "tempmonitor.dmg"
  br = mechanize.Browser()
  br.open(url)
  br.select_form(name="Download")
  response1 = br.submit()
  print "Downloading TempMonitor..."
  with open(tempmon_archive, "w") as f:
    f.write(response1.read())
  if sha1:
    # let's verify sha1
    print "Verifying SHA1 checksum...",
    if sha1 == hashlib.sha1(open(tempmon_archive, 'rb').read()).hexdigest():
      print "Success!"
    else:
      print "Failed, this might cause problems later on.."
  return tempmon_archive

def extractTempMonitorArchive(archive):
  # First convert the archive to be able to automatically mount it later
  convert_command = "hdiutil convert -quiet %s -format UDTO -o tempmonitor.cdr" % (archive)
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

def cleanArchives(archive):
  print "Cleaning archive...",
  basename = archive.split('.')[0]
  # remove both archives
  os.remove(basename+'.cdr')
  os.remove(basename+'.dmg')
  print "Done!"


def main():
  tempmonitor_url = 'http://www.bresink.de/osx/0TemperatureMonitor/download.php5'
  tempmon_sha1 = getSHA1forTempmonitor(tempmonitor_url)
  tempmon_archive = downloadTempMonitor(tempmonitor_url, tempmon_sha1)
  extractTempMonitorArchive(tempmon_archive)
  cleanArchives(tempmon_archive)


if __name__ == '__main__':
  main()