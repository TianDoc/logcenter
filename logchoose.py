import subprocess
import time
import pymysql
import pymysql.cursors
import smtplib
import logging
import email.mime.multipart    
import email.mime.text    
from collections import deque
import redis
import time
import base64
import os
import threading
import traceback


His_Sendnum = 2000          ###历史记录储存上限
Mis_Sendnum = 1             ###错误日志储存上限
pwd = "/usr/local/logtest/untitled2/logcenter/"

importantip=[]        ###将重要的报警IP提取出来
for line in open("%sip.txt" %pwd):
    importantip.append(line.replace('\n',''))


def timechange(timedate):               ###将日志时间信息转换为DateTime
    a=timedate+" "+str(time.localtime(time.time())[0])
    return str(time.mktime(time.strptime(a,"%b %d %H:%M:%S %Y")))

def sqloperate(data):
    if data == 'control':                          ###从数据库中读取赛选条件
        sql="select * from showlog_control order by power desc"
    elif data == 'discard':                         ###从数据库中读取过滤条件
        sql = "select * from showlog_discard"
    else:                                        ###从数据库中取出邮箱地址
        sql='SELECT emailaddress FROM showlog_user where groupname= "'+data+'" '
    return sqlreturn(sql)

def save(data,type):
    conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
    cur = conn.cursor()
    if type == 'historytable':
        for p in data:
            sql="INSERT INTO showlog_historytable(DATE,TIME,HOST)VALUES('"+p[0]+"','"+p[1].split('.')[0]+"','"+p[2]+"')"
            cur.execute(sql)
    elif type == 'table':
        for p in hehe:
            sql="INSERT INTO showlog_table(DATE,TIME,NAME,HOST,question,showmessage)VALUES('"+p[0]+"','"+p[1].split('.')[0]+"','"+p[2]+"','"+p[3]+"','"+p[4]+"','"+p[5]+"')"
            cur.execute(sql)
    cur.close()
    conn.commit()           ###利用事务来提高插入性能
    conn.close()

def sqlreturn(sql):                     ###数据库操作有返回值，select
    conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              cursorclass = pymysql.cursors.DictCursor,
                              charset='utf8')
    cur = conn.cursor()
    date=cur.fetchmany(cur.execute(sql))
    cur.close()
    conn.commit()
    conn.close()
    return date

def sendmail2(host,message,time,question,name):                         ###发送邮件函数
    if question.strip()!='up' and question.strip()!='down':
        subject=" "+'"'+"[日志告警]"+host+"  "+question+"  "+time+'"'
        message=' '+'"'+message+'"'
        for i in sqloperate(name):
            os.system('sh %smailsend.sh %s%s%s' %(pwd,i['emailaddress'],subject,message))
    else:
        if host in importantip:
            subject=" "+'"'+"[日志告警]"+host+"  "+"端口up/down"+"  "+time+'"'
            #subject=" "+(host+question+time).replace(" ","。").replace("/","/").replace("<","《").replace(">","》").replace(";","；")
            message=' '+'"'+message+'"'
            for i in sqloperate(name):
                os.system('sh %smailsend.sh %s%s%s' %(pwd,i['emailaddress'],subject,message))
        
def getresult(host,message,realtime,question,times,name,showmessage):              ###报警模块
    global he
    global hehe
    if host+question in he:
        he[host+question][1]+=1
    else:
        he[host+question]=[message,1,time.time(),0]
    if he[host+question][1] >=times:                                    #发送报警
        if  he[host+question][3]==0 and time.time()-he[host+question][2]<300: 
            t=threading.Thread(target=sendmail2,args=[host,message,realtime,question,name])
            t.start()
            he[host+question][3]=1
        elif time.time()-he[host+question][2]>=300:
            t=threading.Thread(target=sendmail2,args=[host,message,realtime,question,name])
            t.start()
            he[host+question][2]=time.time()
        he[host+question][1]=0
    hehe.append([message,timechange(realtime),name,host,question,showmessage])    #将报警信息添加到list中

def cuttext(text):
    return text.split(",")

def screen():                  ###逻辑筛选模块
    global hehe
    global hehehe
    r=redis.Redis(host='10.21.8.37',port=6379,db=0,password="@_redis&redis_@")
    question=sqloperate('control')
    discard=sqloperate('discard')
    time_start=time.time()
    count=0
    whatiwant=1
    while True:
        p=eval(r.brpop("logstash",0)[1])
        host=p["host"]
        try:
            rtime=p["timestamp"]
            message=p["message"][1].replace("'"," ")
            for discards in discard:
                if discards['keyword'] in message:
                    whatiwant=0
            if whatiwant:
                hehehe.append([message,timechange(rtime),host])
                count+=1
                for questions in question:
                    if questions["keyword"] in message or questions["keyword"].upper() in message or questions["keyword"].lower() in message  or questions["keyword"].capitalize() in message:
                        if questions["nokeyword"]!='':
                            x=cuttext(questions["nokeyword"])
                            for i in x:
                                if i in message or i.upper() in message or i.lower() in message or i.capitalize() in message:
                                    break
                            else:
                                getresult(host,message,rtime,questions["keyword"],questions["times"],questions["contactsname"],questions["showmessage"])
                        else:        
                            getresult(host,message,rtime,questions["keyword"],questions["times"],questions["contactsname"],questions["showmessage"])
                        break
            whatiwant=1
        except:
            pass 
        if time.time()-time_start>60:
            question=sqloperate('control')  ###每隔1分钟重新加载一次塞选条件
            time_start=time.time()
        try:
            if count >His_Sendnum:          ###当存His_Sendnum条错误日志时统一添加到数据库
                save(hehehe,'historytable')
                count=0
                hehehe.clear()
        except:
            print("存历史信息出错")
            print(hehehe[-10:-1])
            hehehe.clear()
            count=0
        if len(hehe)>=Mis_Sendnum:     ###当存Mis_Sendnum条错误日志时统一添加到数据库
            save(hehe,'table') 
            hehe.clear()    


def printifeng():
    banner = 'IF8gIF9fCihfKS8gX3wgX19fIF8gX18gICBfXyBfCnwgfCB8XyAvIF8gXCAnXyBcIC8gX2AgfAp8IHwgIF98ICBfX' \
             'y8gfCB8IHwgKF98IHwKfF98X3wgIFxfX198X3wgfF98XF9fLCB8CiAgICAgICAgICAgICAgICAgIHxfX18vCg=='
    print  (base64.b64decode(banner).decode())

if __name__ == '__main__': 
     global hehe                     ##储存所有报警list                    
     global he                       ##记录报警出现次数的字典
     he={}
     hehe=deque([])
     hehehe=deque([])
     print('雷霆日志系统启动啦')
     printifeng()
     t=threading.Thread(target=sendmail2,args=["1","1","1","1","测试组"])
     t.start()
     try:
         screen()
     except:
         sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")