#!/usr/bin/env python3
#-*- coding; utf-8 -*-

#####################\
# XRDownloader v1.0.2
#####################/

#----------------------------------------------------------------------------
# MIT License

# Copyright (c) 2019 XploitsR

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#------------------------------------------------------------------------------

import urllib3
import certifi
import os,time
import sys,re

def rawincount(filename):
    num_lines = 0
    with open(filename) as f:
      for line in f:
        if len(line.strip()) < 1:
          continue
        else:
          num_lines += 1
    return num_lines

def pre(arg):
  print("""
##############################################################|
#   [+] Preparing to download-->({0})->file(s)
##############################################################|
""".format(arg))
  time.sleep(2)

def main(xrurl,typeO):
        #check if input is a list
        if type(xrurl) != list:
           try:  
            check_usrF = os.path.isfile(xrurl)
           except:
             check_usrF = False
            #Check if xrurl is a file
           if check_usrF == True:
              f = open(str(xrurl))
              if len(str(f)) > 0:
                pre(rawincount(xrurl))
                xrurl = f
           else:
              pre(len([xrurl]))
              xrurl = [xrurl]
        elif type(xrurl) == list:
           pre(len(xrurl))
           xrurl = xrurl
        #start iterating
        for url in xrurl:
          if len(url.strip()) < 1:
             continue
          url_split = str(url.strip()).split("/")
          if len(str(url_split[-1]).strip()) < 1:
             url_split[-1] = "Unknown!"
          print("""
##############################################################|
[+] Downloading-->{0}                      
##############################################################|
                """.format(str(url_split[-1])))
          http = urllib3.PoolManager(
          cert_reqs='CERT_REQUIRED',
          ca_certs=certifi.where())
          data = http.request('GET',url.strip())
          if data.status == 200:
           if str(url.strip()) is not None:
            check_Fexists = os.path.isfile(str(url_split[-1]))
            if check_Fexists == True:
                 print("[!] {0} file already exists".format(str(url_split[-1])))
                 print("[>] please do you want to overwrite it? yes/no")
                 usr = str(input("[#] >>>: "))
                 #verify
                 if len(usr.strip()) > 0 and usr.lower().strip() == "yes":
                    start = True
                    print(" ")
                    print("[O] ok->Overwriting({0})".format(str(url_split[-1])))
                 elif len(usr.strip()) > 0 and usr.lower().strip() == "no":
                    print(" ")
                    print("[>] Or do you want to rename it? yes/no")
                    usr = str(input("[#] >>>: "))
                    if len(usr.strip()) > 0 and usr.lower().strip() == "yes":
                       #Generate random alphanumeric char
                       import random,string
                       start = True
                       print(" ")
                       print("[R] ok->Renaming({0})".format(str(url_split[-1])))
                       ran = random.SystemRandom()
                       lent = 4
                       ch = "abcdefghijklmnopqrstuvwxyz" + string.digits
                       ranNum = str().join(ran.choice(ch) for _ in range(lent))
                       url_split[-1] = "{0}-{1}".format(ranNum,url_split[-1])
                    elif len(usr.strip()) > 0 and usr.lower().strip() == "no":
                       print("[S] ok->Skipped({0})".format(str(url_split[-1])))
                       continue
                    else:
                       print("Don't be silly, choose from above list")
                       quit()
                 else:
                    print("Don't be silly, choose from above list")
                    quit()
                 #procced if yes
                 if start == True:
                  with open(str(url_split[-1]),typeO) as f:
                    if f is not None:
                      f.write(data.data)
                      time.sleep(0.5)
                      print("[*] downloaded->{0}".format(str(url_split[-1])))
                      f.close()
            else:
                 with open(str(url_split[-1]),typeO) as f:
                   if f is not None:
                    f.write(data.data)
                    time.sleep(0.5)
                    print("[*] downloaded->{0}".format(str(url_split[-1])))
                    f.close()
          elif data.status == 404:
           print("[!] DownloadError: File not found")
           quit()
          else:
           print("HTTPError: Couldn't fetch data,retry ")
           quit()

class XRDownloader:
   def download_Files(self,xrurl):
      try:
        typeO = "wb"
        main(xrurl,typeO)
        pass
      except Exception as e:
        if str(e).lower() == 'write() argument must be str, not bytes':
          typeO = "w"
          main(xrurl,typeO)
        elif re.search("port=80",str(e).lower()):
          print("[!]DownloadError: Cant download such file(s)")
          quit()
        elif re.search("port=443",str(e).lower()):
          print("[!]NetworkError: Failed to establish a network connection")
          quit()
        else:
          print(e)
          quit()
      except KeyboardInterrupt:
        print("Exiting...")
        quit()
      time.sleep(1)
      return "[^] Done (^_^)"

if __name__ == '__main__':
   sys.exit()
