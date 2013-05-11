#!/usr/bin/env python
#
# Use this script to download and extract the dependency binaries
#

import urllib2
from bs4 import BeautifulSoup
import re
import mechanize
import hashlib

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
  with open(tempmon_archive, "w") as f:
    print "Downloading TempMonitor..."
    f.write(response1.read())
  if sha1:
    # let's verify sha1
    print "Verifying SHA1 checksum...",
    if sha1 == hashlib.sha1(open(tempmon_archive, 'rb').read()).hexdigest():
      print "Success!"
    else:
      print "Failed, this might cause problems later on.."

def main():
  tempmonitor_url = 'http://www.bresink.de/osx/0TemperatureMonitor/download.php5'
  tempmon_sha1 = getSHA1forTempmonitor(tempmonitor_url)
  downloadTempMonitor(tempmonitor_url, tempmon_sha1)

if __name__ == '__main__':
  main()