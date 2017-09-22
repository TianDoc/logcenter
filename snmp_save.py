import os
import logchoose
import time

Limit_Num = 99
Host = {}
def FindHost(id):
    return Host['id'] if id in Host else "123456"


table = []
historytable = []
datas = os.popen('snmpwalk -c Lx6X1yiy -v 2c  172.31.150.252 1.3.6.1.4.1.25506.2.75.2.2.3.1.6').readlines()
rtime = str(int(time.time()))

for data in datas:
    host = FindHost("data.split('= INTEGER:')[0].strip()")
    if int(data.split('= INTEGER:')[1].strip()) >= Limit_Num:
        table.append([data,rtime,host,host,"snmp","AP当前关联STA数量"])
        logchoose.sendmail2(host[:-1],data,rtime,"snmp","AP组")
    historytable.append([data[:-1],rtime,host])
# print (table)
# print (historytable)
if table:
    logchoose.save(table,"table")
if historytable:
    logchoose.save(historytable,"historytable")