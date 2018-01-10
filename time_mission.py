#****************************************************************#
# ScriptName: logcenter crontab control module
# version 1.0.1
# Author:
# Create Date: 2017-09-27
# Modify Author: zhangpc1@ifeng.com
# Modify Date: 2017-09-27
# Function: control logcenter crontab
#***************************************************************#
import os
from multiprocessing import Process
import time
import operate
import logchoose
import snmp_save
import base64
import snmp_check

pwd = "/usr/local/logtest/untitled2/logcenter/"
###加载需要启动的进程 每种日志收集方式 开辟一条进程
ps1 = Process(target = logchoose.run)
ps2 = Process(target = snmp_check.run)


def alive_check():       ###进程检测模块
    global ps1,ps2
    if not ps1.is_alive():
        ps1 = Process(target = logchoose.run)
        ps1.start()
    if not ps2.is_alive():
        ps2 = Process(target = snmp_check.run)
        ps2.start()

def kill_all():
    global ps1,ps2
    if  ps1.is_alive():
        ps1.terminate()
    if  ps2.is_alive():
        ps2.terminate()
def printifeng():
    banner = 'IF8gIF9fCihfKS8gX3wgX19fIF8gX18gICBfXyBfCnwgfCB8XyAvIF8gXCAnXyBcIC8gX2AgfAp8IHwgIF98ICBfX' \
             'y8gfCB8IHwgKF98IHwKfF98X3wgIFxfX198X3wgfF98XF9fLCB8CiAgICAgICAgICAgICAgICAgIHxfX18vCg=='
    print  (base64.b64decode(banner).decode())

if __name__ == '__main__':
    print('雷霆日志系统启动啦')
    printifeng()
    alive_check()
    try:
        while True:
            alive_check()
            time.sleep(30)
    except:
        kill_all()