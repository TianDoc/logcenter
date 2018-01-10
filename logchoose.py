#####
##logstash 获取日志存到数据库方式
##
#####
import subprocess
import time 
from collections import deque
import redis
import time
import os
import threading
import traceback
import operate
import json

Session_Sendnum = 20000      ###Session储存上限
His_Sendnum = 2000          ###历史记录储存上限
Mis_Sendnum = 1             ###错误日志储存上限
pwd = "/usr/local/logtest/untitled2/logcenter/"




def timechange(timedate):               ###将日志时间信息转换为时间戳
    if isinstance(timedate,float):
        return str(timedate)
    a=timedate+" "+str(time.localtime(time.time())[0])
    return str(time.mktime(time.strptime(a,"%b %d %H:%M:%S %Y")))




        
def getresult(host,message,realtime,question,times,name,showmessage):              ###报警模块
    global he
    global hehe
    if host+question in he:
        he[host+question][1]+=1
    else:
        he[host+question]=[message,1,time.time(),0]
    if he[host+question][1] >=times:                                    #发送报警
        if  he[host+question][3]==0 and time.time()-he[host+question][2]<300: 
            t=threading.Thread(target=operate.sendmail2,args=[host,message,realtime,question,name])
            t.start()
            he[host+question][3]=1
        elif time.time()-he[host+question][2]>=300:
            t=threading.Thread(target=operate.sendmail2,args=[host,message,realtime,question,name])
            t.start()
            he[host+question][2]=time.time()
        he[host+question][1]=0
    hehe.append([message,timechange(realtime),name,host,question,showmessage])    #将报警信息添加到list中

def cuttext(text):
    return text.split(",")

def screen():                  ###逻辑筛选模块
    global hehe
    global hehehe
    global hehehehe
    r=redis.Redis(host='10.21.8.37',port=6379,db=0,password="@_redis&redis_@")
    question=operate.sqloperate('control')
    discard=operate.sqloperate('discard')
    time_start=time.time()
    count=0
    count_session=0
    whatiwant=1
    while True:
        p=eval(r.brpop("logstash",0)[1])
        host=p["host"]
        try:
            if 'timestamp' not in p:
                rtime = time.time()
            else:
                rtime=p["timestamp"]
            if type(p["message"]) == list:
                message=p["message"][1].replace("'"," ")
            elif type(p["message"]) ==str:
                whatiwant=0
                message=p["message"].replace("'"," ")
            if 'session start' in message :
                #print(message)
                hehehehe.append([message,timechange(rtime),host])
                count_session+=1
            if whatiwant:
                for discards in discard:
                    if discards['keyword'] in message:
                        whatiwant=0
            if host == "10.0.21.13":
                whatiwant=1
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
            traceback.print_exc()
        if time.time()-time_start>60:
            question=operate.sqloperate('control')  ###每隔1分钟重新加载一次塞选条件
            time_start=time.time()
        if count_session>Session_Sendnum:
            try:
                #operate.save_session(hehehehe)
                #t=threading.Thread(target=operate.save_session,args=[hehehehe])
                #t.start()
                #t.join()
                count_session=0
                hehehehe=[]
            except:
                operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
                count_session=0
                hehehehe.clear()
        if count >His_Sendnum:          ###当存His_Sendnum条错误日志时统一添加到数据库
            try:
                operate.save(hehehe,'historytable')
                count=0
                hehehe.clear()
            except:
                operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
                hehehe.clear()
                count=0
             # operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
        if len(hehe)>=Mis_Sendnum:     ###当存Mis_Sendnum条错误日志时统一添加到数据库
            operate.save(hehe,'table') 
            hehe.clear()    

def run(): 
    global hehehehe
    global hehehe
    global hehe                     ##储存所有报警list                    
    global he                       ##记录报警出现次数的字典
    he={}
    hehe=[]
    hehehe=[]
    hehehehe=[]
    t=threading.Thread(target=operate.sendmail2,args=["1","1","1","1","测试组"])
    t.start()
    try:
        screen()
    except:
        operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
