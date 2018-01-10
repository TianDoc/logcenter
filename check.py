import subprocess
import time
import datetime
import logging
import os
import threading
import traceback
def getresult():
    print("test")
    times=str(datetime.datetime.now())
    os.system("python3 /usr/local/logtest/untitled2/logcenter/time_mission.py&")
    os.system("sh /usr/local/logtest/untitled2/logcenter/mailsend.sh 'zhangpc1@ifeng.com' '进程重启了' '进程重启了'")    
def getresult2():
    f = os.popen("ps -ef|grep mission").reads()
    os.system("sh /usr/local/logtest/untitled2/logcenter/mailsend.sh 'zhangpc1@ifeng.com' '貌似有进程掉了' %s"%f)
getresult() if int(os.popen("ps -ef|grep mission|wc -l").read()[:-1].strip()) <=2 else ""   ####在os中的管道加管道符 实际上会产生两个进程
getresult2() if int(os.popen("ps -ef|grep mission|wc -l").read()[:-1].strip()) !=5 else ""
#time.sleep(300)
