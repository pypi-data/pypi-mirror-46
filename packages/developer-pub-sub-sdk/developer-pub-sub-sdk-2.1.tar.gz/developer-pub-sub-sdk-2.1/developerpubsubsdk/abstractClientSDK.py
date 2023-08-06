import json
import select
import struct
import datetime
import threading
import time
import warnings
import sys
import os
from threading import Thread
import ssl
import socket
from queue import Queue
import six
from twisted.internet.protocol import Protocol
from .bean import SubscripProtos_pb2, PublishProtos_pb2
from .src.config import SDKConfig
from .src.httpResult import result

global subClientHandler
subClientHandler = None





class AbstractClientSDK(Protocol):
      PARSING_LEN = 0
      PARSING_MSG = 1
      send_queue  = Queue()
      su_bean     = Queue()
      mess_queue  = Queue()
      put_queue   = Queue()
      init_sub_flag = False
      topic       = ""
      number_line = 3
      lock = threading.RLock()
      ZERO        = 0
      ONE         = 1
      array_bytes = Queue()
      RECV_BUF_SIZE = 409600
      RESULT_QUEUE  = Queue()
      def __init__(self,config):
          try:
              if not config:
                 raise RuntimeError("Parameter is wrong")
          except Exception as  e:
              print(e)
              exit()
          self._config = config
          self.data_buffer = b""
          self.parse_status = self.PARSING_LEN
          self.msg_len = 0
          self.num  = 0

      """
      連接服務器
      """
      def connect(self,subCallback="",pubCallback=""):
          self._pubCallback = pubCallback
          self._subCallback = subCallback
          self.login()
          self.connects(self.getPubSubServer(),self.getTcpPort())
      """
      獲取token
      """
      def login(self):
          dataArray = {
              SDKConfig.CLIENT_ID:self.getClientId(),
              SDKConfig.SECRET_KEY:self.getSecret()
          }

          token =  result.post(self.getHttpServer(),dataArray)
          self.setToken(token)

      """
      初始化连接
      """
      def connects(self,host,port):
          timeout = 900
          global subClientHandler
          # subClientHandler = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          subClientHandler = ssl.wrap_socket(socket.socket())
          subClientHandler.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
          subClientHandler.settimeout(timeout)
          # subClientHandler.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,self.RECV_BUF_SIZE)
          addr = (socket.gethostbyname(host),port)
          try:
                  self.num += 1
                  if subClientHandler.connect_ex(addr) != self.PARSING_LEN:
                      if self.num == 10000:
                          exit()
                      time.sleep(20)
                      print("重新连接中======")
                      self.connect("","")

                  self.activate()
          except:
            subClientHandler.close()
            raise RuntimeError("tcp connects to  fails ")
      """
      发布消息
      """
      def backPublish(self,topic,jsonData):
          self.validate()
          pro = PublishProtos_pb2.ProtocolEnum.items()
          data = self.builderPubBean(dict(pro)["BACKPUB"], topic, jsonData)
          self.send(data)
      """
      订阅
      """
      def subscript(self, topic=""):
          warnings.filterwarnings("ignore")
          self.validate()
          pro = PublishProtos_pb2.ProtocolEnum.items()
          data = self.builderPubBean(dict(pro)["SUB"], topic, "")
          self.senSug(data)
          self.topic   = topic
          self.init_sub_flag = True
          self.send(data)

      """
       发布消息
      """
      def publish(self, jsonData):
          self.validate()
          pro = PublishProtos_pb2.ProtocolEnum.items()
          data = self.builderPubBean(dict(pro)["PUB"], "", jsonData)
          self.send(data)
      """
      檢查機制
      """
      def validate(self):
          if(subClientHandler == None):
             raise RuntimeError("请求先调用connect方法")

      """
      获取的消息
      """
      def builderPubBean(self,number,topic,data):
          publish =  PublishProtos_pb2.PublishBean()
          publish.token = "*"
          publish.topicPath = topic
          publish.protocolType = number
          publish.body   = data
          return publish

      """
      用protobuf的協議定義格式
      """
      def builderPubBeanToken(self,number):
          publish = PublishProtos_pb2.PublishBean()
          publish.token = self.getToken()
          publish.protocolType = number
          return publish

      """
      连接
      """
      def activate(self):
             print("--------------连接激活"+str(self.num)+"次--------------")
             print("--------------完成订阅--------------")
             self.num += 1
             pro = PublishProtos_pb2.ProtocolEnum.items()
             dataConn = self.builderPubBeanToken(dict(pro)["CONN"])
             self.send(dataConn)
             if self.init_sub_flag == True:
                 pro = PublishProtos_pb2.ProtocolEnum.items()
                 data = self.builderPubBean(dict(pro)["SUB"], self.topic, "")
                 self.sendSig(data)
                 self.su_bean = data
                 subClientHandler.sendall(self.su_bean.get() + self.su_bean.get())
                 result = subClientHandler.recv(1024)
                 if result not  in -1:
                     self.analysis(result)
                 else:
                     self.connects(self.getPubSubServer(), self.getTcpPort())

      """
      給服務端發送消息，然後在接收返回消息
      """
      def send(self,data):
              self.sendSig(data)
              if self.send_queue.qsize() == self.number_line:
                  subClientHandler.sendall(self.send_queue.get() + self.send_queue.get() + self.send_queue.get())
              else:
                  subClientHandler.sendall(self.send_queue.get() + self.send_queue.get())
              result = subClientHandler.recv(1024)
              self.analysis(result)

      """
      接收服務端返回的消息，用recv，這種模式是阻塞模式，接收的消息不完整，這是個坑，所以要把服務端返回的消息拼接
      """
      def awit(self,num):
              try:
                  result = subClientHandler.recv(4096)
              except  OSError:
                  subClientHandler.close()
                  print("正在重新连接中：")
                  self.restart_program()
              if not result:
                      print("正在重新连接中：")
                      time.sleep(10)
                      subClientHandler.close()
                      self.restart_program()
              else:
                  if ((result[-2:] == b'}]')== True and (result[4:6]  == b'OK')== True):
                      return self.thredaStart(result, num)
                  else:
                      if "}]" not in str(result):
                          if self.RESULT_QUEUE.qsize() == self.ZERO:
                              resuls = bytes()
                          else:
                              resuls = self.RESULT_QUEUE.get()
                          resuls += result
                          self.RESULT_QUEUE.put(resuls)
                          return None
                      else:
                          if (result[4:6] == b'OK') == False:
                              if self.RESULT_QUEUE.qsize() == self.ZERO:
                                  resulsArray = bytes()
                              else:
                                  resulsArray = self.RESULT_QUEUE.get()
                              return self.thredaStart(resulsArray + result, num)
                          else:
                              return self.thredaStart(result, num)



      """
      起個進程,消費者模式
      """
      def thredaStart(self,result,num):
          self.mess_queue.put(result)
          data = Thread(target=self.analysi)
          data.setDaemon(False)
          data.start()
          data.join(1)
          test = Thread(target=self.analysi)
          test.setDaemon(True)
          test.start()
          # test.join(1)
          dataArray = self.proces(num)
          return dataArray




      """
      发的数据前面加消息的长度和消息
      消息的长度编码为 Varint32
      https://blog.csdn.net/lucyTheSlayer/article/details/79722751  可查阅
      """
      def sendSig(self,sig):
        value = len(sig.SerializeToString())
        bits = value & 0x7f
        value >>= 7
        while value:
            self.send_queue.put(six.int2byte(0x80 | bits))
            bits = value & 0x7f
            value >>= 7
        self.send_queue.put(six.int2byte(bits))
        self.send_queue.put(sig.SerializeToString())

      """
      解析返回的数据，這是正常返回的數據
      """
      def  analysis(self, data):
              for b in data:
                  if self.parse_status == self.PARSING_LEN:
                      self.data_buffer += six.int2byte(b)
                      if not (b & 0x80):
                          self.msg_len = self.DecodeVarint(self.data_buffer)
                          self.parse_status = self.PARSING_MSG
                          self.data_buffer = b""
                          continue
                  elif self.parse_status == self.PARSING_MSG:
                      self.data_buffer += six.int2byte(b)
                      if len(self.data_buffer) == self.msg_len:
                          sig = SubscripProtos_pb2.ResultBean()
                          sig.ParseFromString(self.data_buffer)
                          self.process(sig)
                          self.data_buffer = b""
                          self.msg_len = 0
                          self.parse_status = self.PARSING_LEN

      """
        解析返回的数据
        """

      def analysi(self):

          if self.mess_queue.qsize()  != self.ZERO:
                   data = self.mess_queue.get()
                   for b in data:
                      if self.parse_status == self.PARSING_LEN:
                          self.data_buffer += six.int2byte(b)
                          if not (b & 0x80):
                              self.msg_len = self.DecodeVarint(self.data_buffer)
                              self.parse_status = self.PARSING_MSG
                              self.data_buffer = b""
                              continue
                      elif self.parse_status == self.PARSING_MSG:
                          self.data_buffer += six.int2byte(b)
                          if len(self.data_buffer) == self.msg_len:
                              sig = SubscripProtos_pb2.ResultBean()
                              sig.ParseFromString(self.data_buffer)
                              self.put_queue.put(sig)
                              self.data_buffer = b""
                              self.msg_len = 0
                              self.parse_status = self.PARSING_LEN

          else:
              return None


      """
      把返回的數據包裝好
      """
      def proces(self,num):
          if self.put_queue.qsize() != self.ZERO:

                  if self.put_queue.qsize() == self.ONE:
                      sig = self.put_queue.get()
                      try:
                          if sig.message == SDKConfig.ERROR:
                              raise RuntimeError("Insufficient permissions, channel closed ")
                          else:
                              if num == 1:
                                  print("read 接受到服务器消息：")
                                  return sig
                              else:
                                  print("read 接受到服务器消息：")
                                  if (sig.protocolType == 2):
                                      con = {"message": "ok", "protocolType": "SUB", "body": sig.body}
                                      return con
                                  if (sig.protocolType == 1):
                                      con = {"message": "ok", "protocolType": "PUB", "body": sig.body}
                                      return con
                      except Exception as e:
                          subClientHandler.close()
                          print(e)
                  else:
                      # for i in range(self.put_queue.qsize()):
                          sigs = self.put_queue.get()
                      # for sig in sigs:
                          try:
                              if sigs.message == SDKConfig.ERROR:
                                  raise RuntimeError("Insufficient permissions, channel closed ")
                              else:
                                  if num == 1:
                                      print("read 接受到服务器消息：")
                                      return sigs
                                  else:
                                      print("read 接受到服务器消息：")
                                      if (sigs.protocolType == 2):
                                          con = {"message": "ok", "protocolType": "SUB", "body": sigs.body}
                                          return con
                                      if (sigs.protocolType == 1):
                                          con = {"message": "ok", "protocolType": "PUB", "body": sigs.body}
                                          return con
                          except Exception as e:
                              subClientHandler.close()
                              print(e)
          else:
              return None
      """
      判斷一下
      """
      def process(self, sig):
          try:
              if sig.message == SDKConfig.ERROR:
                  raise RuntimeError("Insufficient permissions, channel closed ")
              else:
                  print("read 接受到服务器消息：" + str(sig))
          except Exception as e:
              subClientHandler.close()
              print(e)

      """
      這是一個算法，把返回的數據解包，以防沾包
      """
      def DecodeVarint(self,buffer):
          mask = (1 << 32) - 1
          result_type = int
          result = 0
          shift = 0
          for b in buffer:
              result |= ((b & 0x7f) << shift)
              shift += 7
              if shift >= 64:
                  raise Exception('Too many bytes when decoding varint.')
          result &= mask
          result = result_type(result)
          return result

      """
      把數據進行二進制
      """
      def senSug(self,data):
          value = len(data.SerializeToString())
          bits = value & 0x7f
          value >>= 7
          while value:
              self.su_bean.put(six.int2byte(0x80 | bits))
              bits = value & 0x7f
              value >>= 7
          self.su_bean.put(six.int2byte(bits))
          self.su_bean.put(data.SerializeToString())

      # 重启程序
      def restart_program(self):
              python = sys.executable
              os.execl(python, python, *sys.argv)


      def getPubSubServer(self):
          return SDKConfig.PUB_SUB_SERVER + ""
      def getTcpPort(self):
          return SDKConfig.TCP_PORT
      def getToken(self):
           if SDKConfig.ACCESS_TOKEN  in self._config:
               return self._config[SDKConfig.ACCESS_TOKEN]
           self.login()
      def setToken(self,data):
         self._config[SDKConfig.ACCESS_TOKEN] = data
      def getApiServer(self):
          return SDKConfig.API_SERVER
      def getHttpPost(self):
          return SDKConfig.HTTP_PORT
      def getHttpServer(self):
          return self.getApiServer()
      def getClientId(self):
          return self._config[SDKConfig.CLIENT_ID]
      def getSecret(self):
          return self._config[SDKConfig.SECRET_KEY]
