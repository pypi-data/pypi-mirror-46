# -*- coding: utf-8 -*-
import requests
import hashlib
import json
import os
import time
import ftplib
import datetime
from virus_total_apis import PublicApi as VirusTotalPublicApi
import multiprocessing as mp

key_file = 'key.txt'

file_path = '/mnt/hgfs/capstone/pdf/data/virustotal'

report_path = '/mnt/hgfs/capstone/pdf/data/virustotal/virustotal_report'

hand_path = '/mnt/hgfs/capstone/pdf/data/heuristics'

new_scan = '/mnt/hgfs/capstone/pdf/data/newscan'

key_list = []


def key_list_update():
   with open(key_file, 'r') as f:
       lines = f.readlines()
       for line in lines:
           key_list.append(line.split('\n')[0])


def create_file_list(root):
   ret_list = []
   for path, dirs, files in os.walk(root):
       for file in files:
           if len(file.split(".")) == 1:
               ret_list.append(os.path.join(path, file))
   return ret_list


def virus_request(items):
   _apikey, resource = items[0], items[1]
   _sha = items[1][:-4]

#   f_path = os.path.join(file_path, resource)
   f_path = resource
   if os.path.getsize(f_path) > 32000000:
       os.rename(f_path, os.path.join(hand_path, resource))

   else:
       try:
           vt = VirusTotalPublicApi(_apikey)
           response = vt.rescan_file(_sha)

           if response['response_code'] == 200:
               if response['results']["response_code"] == 1:
                  print("rescan", _sha)

               elif response['results']["response_code"] == 0:
                  os.rename(f_path, os.path.join(new_scan, resource))
           else:
               return items

       except Exception as ep:
           print("Error", ep)

def run():
   print("Start")
   key_list_update()

   start_time = time.time()

   file_list = create_file_list(file_path)

   total = list(zip([key_list[i%len(key_list)] for i in range(len(file_list))], file_list))
   print(len(total))
   p = mp.Pool(4)

   while len(total):
       temp = p.map(virus_request, total)
       total = [ each for each in temp if each != None ]

   print("End \n")
   print("running time : ", time.time() - start_time)

if __name__ == '__main__':
   run()
