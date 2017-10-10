#####
##snmp 获取日志存到数据库方式
##
#####
import os
import time
import threading
import traceback
import operate

pwd = "/usr/local/logtest/untitled2/logcenter/"
HOST={}
snmpcommit = [["snmpwalk -c Lx6X1yiy -v 2c  172.31.150.252 1.3.6.1.4.1.25506.2.75.2.2.3.1.6",90,"AP当前关联STA数量"],\
               ['snmpwalk -c Lx6X1yiy -v 2c  172.31.150.252 1.3.6.1.4.1.25506.2.75.2.1.10.1.7',2,"AP当前状态"] ]
dataline = []
table = []
historytable = []
with open('%sAPhost.txt'%pwd,'r') as f:
    for line in f.readlines():
        HOST[line.split(':')[0].strip()] = [line.split(':')[1].strip(),line.split(':')[2].strip()]

def FindHost(id):
    id = ordchange(id).strip()
    return HOST[id][1]+' : '+HOST[id][0] if id in HOST.keys() else 123456

def ordchange(id):
    return ''.join([chr(int(x)) for x in id.split(".")[-20:]])


def run(): 
    time_start = time.time()
    while True:
        try:
            if time.time()-time_start>300:
                for x in range(len(snmpcommit)):
                    dataline.append(os.popen('%s'%snmpcommit[x][0]).readlines()[:-1])
                rtime = str(int(time.time()))
                for x in range(len(dataline)):
                    for data in dataline[x]:
                        host = FindHost(data.split('= INTEGER:')[0].strip())
                        if int(data.split('= INTEGER:')[1].strip()) >= snmpcommit[x][1]:
                            table.append([data,rtime,"AP组",host,"snmp",snmpcommit[x][2]])
                            t=threading.Thread(target=operate.sendmail2,args=[host[:-1],data,rtime,"snmp","AP组"])
                            t.start()
                        historytable.append([data[:-1],rtime,host])
                time_start = time.time()
                if table:
                    operate.save(table,"table")
                if historytable:
                    operate.save(historytable,"historytable")
                dataline.clear()
                table.clear()
                historytable.clear()
        except:
            operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
        time.sleep(1)