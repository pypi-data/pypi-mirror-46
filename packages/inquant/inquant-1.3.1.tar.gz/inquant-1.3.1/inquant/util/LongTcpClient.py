# -*- coding: utf-8 -*-
import socket
import datetime
import threading
import time
import sys

class LongTcpClient(object):
    """TCP长连接"""
    
    #超时时间
    __Timeout = 30000
    #单条消息终结符
    __EOL = 10

    def __init__(self,host,port,header,recvFn,errorFn):
        """构造函数"""

        #主机Host
        self.host = host
        #端口
        self.port = port
        #消息头
        self.header = header
        #socket连接
        self.client = None
        #最后调用时间
        self.lastCallTime = datetime.datetime.now()
        self.__hasStartReconnect = False
        self.__hasStartRecv = False
        self.__hasStartHb = False
        self.__recvFn = recvFn
        self.__errorFn = errorFn

    def Connect(self):
        "启动连接"

        if self.client:
            return True
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        ret = self.client.connect_ex((self.host,self.port))
        if ret != 0:
            self.client = None
            return False
        
        if self.__hasStartRecv:
            return True
        self.__hasStartRecv = True
        t = threading.Thread(target=self.__ReceiveMsg)
        t.start()
        return True

    def StartHeartBeat(self,content):
        """启动心跳"""
        if not content:
            return False
        if self.__hasStartHb:
            return True
        self.__hasStartHb = True

        t = threading.Thread(target=self.__TimerHeartBeat,args=(content,))
        t.start()
        return True

    def StartAutoReconnect(self):
        """启动心跳"""
        if self.__hasStartReconnect:
            return True
        self.__hasStartReconnect = True

        t = threading.Thread(target=self.__TimerReconnect)
        t.start()
        return True
   
    def Send(self,msg):
        """发送消息"""
        if not msg:
            return False
        if not self.client:
            return False
        length = len(bytes(msg,encoding="utf-8"))
        full = self.header + str(length).zfill(8) + msg
        self.client.send(bytes(full,encoding="utf-8"))
        self.lastCallTime = datetime.datetime.now()
        return True

    def __TimerHeartBeat(self,content):
        while True:
            try:
                self.Send(content)
            except (socket.error,IOError) as e:
                self.__errorFn(e)
                self.client.close()
                self.client = None
                time.sleep(3)
            except Exception as e:
                self.__errorFn(e)
            time.sleep(5)

    def __TimerReconnect(self):
        while True:
            try:
                self.Connect()
            except Exception as e:
                self.__errorFn(e)
            time.sleep(20)

    def __ReceiveMsg(self):
        """接收消息"""

        self.lastCallTime = datetime.datetime.now()
        chunks = []
        while True:
            try:
                if not self.client:
                    time.sleep(1)
                    continue
                if (datetime.datetime.now() - self.lastCallTime).seconds >= self.__Timeout:
                    self.client.close()
                    self.client = None
                    continue
                buf = self.client.recv(4 * 1024 * 1024 - len(chunks))
                if len(buf) <= 0:
                    self.client.close()
                    self.client = None
                    continue
                self.lastCallTime = datetime.datetime.now()
                chunks += buf
                messages,remains = self.__ToMessages(chunks)
                if(len(remains) > 1024 * 1024):
                    remains = []
                chunks = remains
                for msg in messages:
                    try:
                        #消息处理
                        self.__recvFn(msg)
                    except Exception as e:
                        self.__errorFn(e)
            except (socket.error,IOError) as e:
                self.__errorFn(e)
                self.client.close()
                self.client = None
                time.sleep(3)
            except Exception as e:
                self.__errorFn(e)
                time.sleep(3)

    def __ToMessages(self,chunks):
        result = []
        temp = []
        for item in chunks:
            if item == self.__EOL:
                msg = bytes(temp).decode("utf-8") 
                result.append(msg)
                temp.clear()
            else:
                temp.append(item)
        return result,temp

if __name__ == '__main__':
    #新建策略
    client = LongTcpClient("futquantpush.inquant.cn",8986,"IQHQ",None,None)
    client.Connect()
    client.StartAutoReconnect()
    client.StartHeartBeat("867a6d7640da567387b1343a4ca4067aa24204aed8091440877378ace6656a99313dde056406d33f")
    client.Send("867a6d7640da567380452b19eeb2373069e1f34a27795e8c02fce924fd3af23c4e264e4408e3060ada2f0b2f4fe6257f476db7dc4212bf128b188aa075116550f331e1c48ab2e103ba71bf0ca69badf7f3fa910ba12a7e5d16dc578ad8e98700bf71f1b9c085cc5c63003da16181337c974c32509d7fbdd8ed14792f0977b3a21bd625fe4fad6f11e7983a3278229d2e1d029dc5bf49619a860855e2fe9d16166f0ff41a767be1d40a1f9c823ac990387b5d4bc0de4b3dff4f6ea796c3a842653153d41568622d56a01adfa106e919ebf26f2cf7054b14c6cc4bb09bb836e41c4982695ad1ff9aa4a2a49f6deaa023c5a5515bc4a07ea81c2371081a0ca24a3a82bf6b9b9ec7d296b12276af822f2d0e284a75dd280660d834aa1b7363a5306da8f44c69ea47ad05e992e623b515331ac77fc2926ec372a005e2d49b12387bb683445812cb6b13c6982088eb8319156988764ccfbe0683719ac03e61bc4b858fb435e7bceb9799a1f3883e90ea7ecc8dab0187f3b6d3f5ee785abf6026afec4c1f9f19a922b4eafe1c9b8dfe6bd88ae0682d608404939783783ed47f79149beca2e73f98df9796fd1099ad5f9bf3a1a6a569ba3fa82a54e33b3dfa6dbc713bbe2c10dcbf254db5032998e3a3e18db5c25b863317047a0691")
