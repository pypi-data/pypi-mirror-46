#coding=utf-8
import time
import threading
from inquant.util.LogRecord import *
import traceback

class MemCache(object):
    '''内存缓存'''

    def __init__(self):
        '''初始化'''
        self.mem = {}
        self.time = {}
        self.lock = threading.RLock()
        t = threading.Thread(target=self.__checkCache)
        t.start()

    def __checkCache(self):
        """定时检查缓存，清除垃圾数据"""
        while True:
            time.sleep(10)
            if not self.lock.acquire(timeout=0.1):
                LogRecord.writeLog("MemCacheError", '获取锁失败')
                continue
            try:
                for key in list(self.mem.keys()):
                    if self.time[key] != -1 and self.time[key] <= time.time():
                        self.delete(key)
            except Exception as e:
                LogRecord.writeLog("MemCacheError", str(e))
                LogRecord.writeLog("MemCacheError", traceback.format_exc())
            finally:
                self.lock.release()

    def set(self, key, data, age=-1):
        '''保存键为key的值，时间位age'''
        if not self.lock.acquire(timeout=0.1):
            LogRecord.writeLog("MemCacheError", '获取锁失败')
            return False
        try:
            self.mem[key] = data
            if age == -1:
                self.time[key] = -1
            else:
                self.time[key] = time.time() + age
            return True
        finally:
            self.lock.release()

    def get(self,key):
        '''获取键key对应的值'''
        if not self.lock.acquire(timeout=0.1):
            LogRecord.writeLog("MemCacheError", '获取锁失败')
            return None
        try:
            if key in self.mem.keys():
                if self.time[key] == -1 or self.time[key] > time.time():
                    return self.mem[key]
                else:
                    self.delete(key)
                    return None
            else:
                return None
        finally:
            self.lock.release()

    def delete(self,key):
        '''删除键为key的条目'''
        if not self.lock.acquire(timeout=0.1):
            LogRecord.writeLog("MemCacheError", '获取锁失败')
            return True
        try:
            if key in self.mem.keys():
                del self.mem[key]
            if key in self.time.keys():
                del self.time[key]
            return True
        finally:
            self.lock.release()

    def clear(self):
        '''清空所有缓存'''
        if not self.lock.acquire(timeout=0.1):
            LogRecord.writeLog("MemCacheError", '获取锁失败')
            return
        try:
            self.mem.clear()
            self.time.clear()
        finally:
            self.lock.release()
