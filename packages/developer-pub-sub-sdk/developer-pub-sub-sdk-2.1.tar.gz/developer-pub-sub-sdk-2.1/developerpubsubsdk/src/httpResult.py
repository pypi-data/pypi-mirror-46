import json
import os
import sys
import time
import requests
from requests.adapters import HTTPAdapter
from .config import SDKConfig


"""
这是http  
获取token
"""
class result:
      def post(url,data):
          s = requests.Session()
          s.mount('http://', HTTPAdapter(max_retries=100000))
          s.mount('https://', HTTPAdapter(max_retries=100000))

          try:
              result = s.post(url + SDKConfig.LOGIN_URL,json=data,headers=SDKConfig.header,timeout=80).text
              dataArray = json.loads(result)
              try:
                  if dataArray["success"] == SDKConfig.SUCCESS:
                     return dataArray["data"]
                  else:
                      raise RuntimeError("Token fetch failed ")
              except:
                  raise RuntimeError("Token fetch failed ")
          except requests.exceptions.RequestException as e:
              python = sys.executable
              os.execl(python, python, *sys.argv)
