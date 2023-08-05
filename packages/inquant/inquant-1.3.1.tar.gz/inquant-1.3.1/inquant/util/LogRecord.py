# -*- coding: utf-8 -*-
import datetime
import os
import traceback

class LogRecord(object):
    """日志帮助类"""

    __logPath = os.path.dirname(__file__)

    def setLogPath(logPath):
        '''设置日志目录'''
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        LogRecord.__logPath = logPath

    def __writeFile(fileName,log):

        if not fileName.endswith('.log'):
            fileName += '.log'
        filePath = LogRecord.__logPath + datetime.datetime.now().strftime("%Y%m%d_%H_") + fileName

        log = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ' + str(log) + '\n'
        with open(filePath, 'a') as f:
            f.write(log)

    def writeLog(fileName,msg,isPrint = True):
        try:
            if isPrint:
                print(msg)
            LogRecord.__writeFile(fileName,msg)
        except Exception as e:
            tracelog = traceback.format_exc()
            print(msg + tracelog)
       
if __name__ == '__main__':
    #新建策略
    LogRecord.setLogPath("d:/home/logs/")
    idx = 0
    while idx < 10000:
        LogRecord.writeLog("logtest",idx)
        LogRecord.writeLog('testerror',idx)
        idx = idx + 1
    print('end of logger')