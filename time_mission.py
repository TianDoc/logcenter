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

pwd = "/usr/local/logtest/untitled2/logcenter/"
Pro = []                    ###加载需要启动的进程 每种日志收集方式 开辟一条进程
ps1 = Process(target = logchoose.run)
ps2 = Process(target = snmp_save.run)
Pro.append(ps1)
Pro.append(ps2)

def alive_check(Pro):       ###进程检测模块
    for ps in Pro:
        if not ps.is_alive():
            ps.start()

def printifeng():
    banner = 'IF8gIF9fCihfKS8gX3wgX19fIF8gX18gICBfXyBfCnwgfCB8XyAvIF8gXCAnXyBcIC8gX2AgfAp8IHwgIF98ICBfX' \
             'y8gfCB8IHwgKF98IHwKfF98X3wgIFxfX198X3wgfF98XF9fLCB8CiAgICAgICAgICAgICAgICAgIHxfX18vCg=='
    print  (base64.b64decode(banner).decode())

if __name__ == '__main__':
    print('雷霆日志系统启动啦')
    printifeng()
    for ps in Pro:
        ps.start()
    while True:
        alive_check(Pro)
        time.sleep(30)