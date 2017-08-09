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

importantip=[]        ###将重要的报警IP提取出来
for line in open("/usr/local/logtest/ip.txt"):
    importantip.append(line.replace('\n',''))


def timechange(timedate):               ###将日志时间信息转换为DateTime
    a=timedate+" "+str(time.localtime(time.time())[0])
    return str(time.mktime(time.strptime(a,"%b %d %H:%M:%S %Y")))

def getcontrol():                       ###从数据库中读取赛选条件
    sql="select * from showlog_control order by power desc"
    return sqlreturn(sql)

def getemailaddress(user):              ###从数据库中取出邮箱地址
    sql='SELECT emailaddress FROM showlog_user where groupname= "'+user+'" '
    return sqlreturn(sql)

def save():                 #存入数据库###利用事务的特性来提高插入性能
    global hehe
    conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
    cur = conn.cursor()
    for p in hehe:
        #print (p)
        sql="INSERT INTO showlog_table(DATE,TIME,NAME,HOST,question,showmessage)VALUES('"+p[0]+"','"+p[1].split('.')[0]+"','"+p[2]+"','"+p[3]+"','"+p[4]+"','"+p[5]+"')"
        cur.execute(sql)
    cur.close()
    conn.commit()           ###利用事务来提高插入性能
    conn.close()
    hehe.clear()
def save2():
    global hehehe
    conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
    cur = conn.cursor()
    for p in hehehe:
        #print (p)
        sql="INSERT INTO showlog_historytable(DATE,TIME,HOST)VALUES('"+p[0]+"','"+p[1].split('.')[0]+"','"+p[2]+"')"
        cur.execute(sql)
    cur.close()
    conn.commit()           ###利用事务来提高插入性能
    conn.close()
    hehehe.clear()

def sqlnoreturn(sql):                    ###数据库操作无返回值，insert，create，update
    conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()           
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
        for i in getemailaddress(name):
            x=subprocess.getoutput('sh /usr/local/logtest/mailsend.sh %s%s%s' %(i['emailaddress'],subject,message))
    else:
        if host in importantip:
            subject=" "+'"'+"[日志告警]"+host+"  "+"端口up/down"+"  "+time+'"'
            #subject=" "+(host+question+time).replace(" ","。").replace("/","/").replace("<","《").replace(">","》").replace(";","；")
            message=' '+'"'+message+'"'
            for i in getemailaddress(name):
                x=subprocess.getoutput('sh /usr/local/logtest/mailsend.sh %s%s%s' %(i['emailaddress'],subject,message))
        
def getresult(host,message,realtime,question,times,name,showmessage):              ###对符合条件的错误信息进行处理
    global he
    global hehe
    if host+question in he:
        he[host+question][1]+=1
    else:
        he[host+question]=[message,1,time.time(),0]
    if he[host+question][1] >=times:                                    #发送报警
        #print(time.time()-he[host+question][2])
        #print(he[host+question])
        if  he[host+question][3]==0 and time.time()-he[host+question][2]<300: 
            sendmail2(host,message,realtime,question,name)
            he[host+question][3]=1
        elif time.time()-he[host+question][2]>=300:
            sendmail2(host,message,realtime,question,name)
            he[host+question][2]=time.time()
        he[host+question][1]=0
    hehe.append([message,timechange(realtime),name,host,question,showmessage])    #将报警信息添加到list中

def cuttext(text):
    return text.split(",")

def screen():                  ###读取redis信息并进行判断
    global hehe
    global hehehe
    r=redis.Redis(host='10.21.8.37',port=6379,db=0,password="@_redis&redis_@")
    question=getcontrol()
    time_start=time.time()
    count=0
    while True:
        p=eval(r.brpop("logstash",0)[1])
        host=p["host"]
        try:
            rtime=p["timestamp"]
            message=p["message"][1].replace("'"," ")
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
        except:
            #print (p)
            #sendmail2(host,p['message'][0],rtime,"异常测试","测试组")
            pass
        if time.time()-time_start>60:
            question=getcontrol()  ###每隔20分钟重新加载一次塞选条件
            time_start=time.time()
        try:
            if count >2000:
                start_time=time.time()
                save2()
                count=0
                print(time.time()-start_time)
        except:
            print("存历史信息出错")
            print(hehehe[-10:-1])
            hehehe.clear()
            count=0
        save() if len(hehe)>=1 else ""      ###当存到600条日志时统一添加到数据库


if __name__ == '__main__': 
     global hehe                     ##储存所有报警list                    
     global he                       ##记录报警出现次数的字典
     he={}
     hehe=deque([])
     hehehe=deque([])
     print('雷霆日志系统启动啦')
     sendmail2("1","1","1","1","测试组")
     screen()
    

                         


