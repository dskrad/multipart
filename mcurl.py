#!/usr/bin/env python
# encoding: utf-8
from subprocess import check_output, Popen
from shutil import copyfileobj
from os import remove
from datetime import datetime
from time import sleep
import sys

def get_filesize(url):
  """Uses curl to retrieve the http headers for supplied
  url. Returns filesize as an int."""
  curl = ["curl", "-I", "-s", url]
  headers = check_output(curl).splitlines()
  content_length = [x for x in headers if "Content-Length:" in x]
  return int(content_length[0].split()[1])

def multi_curl(destination, url, num_parts=10):
  """Uses multiple curl instances to download supplied url
  into multiple parts, then combines these temporary files
  into destination file, removing temporary files."""
  size = get_filesize(url)
  chunks, calls, parts= [], [], []
  for i in range(num_parts):
    chunk_size = size/num_parts
    x = i * chunk_size
    y = ((i+1) * chunk_size) - 1
    if i < (num_parts-1):
      chunks.append("{}-{}".format(x,y))
    else:
      chunks.append("{}-{}".format(x,y+1))
    parts.append("tempfile_part{}".format(i))
  start = datetime.now()
  print "{} Starting multiple curl downloads".format(start)
  for part, chunk in zip(parts, chunks):
    calls.append(Popen(["curl", "-s", "-o", part, "-r", chunk, url]))
    sleep(2)
  status = [p.wait() for p in calls]
  print "{} downloaded in {} seconds".format(
         (destination, datetime.now()-start).seconds)
  with open(destination, "wb") as dest:
    for part in parts:
      with open(part, "rb") as part_:
        print "Copying {} to {}".format(part, destination),
        copyfileobj(part_, dest)
      print "deleting {}".format(part)
      remove(part)
  return status

if __name__ == '__main__':
  #multi_curl("file.zip", "http://download.thinkbroadband.com/50MB.zip")
  multi_curl(sys.argv[1], sys.argv[2])
