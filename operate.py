import pymysql
import pymysql.cursors
import smtplib
import os
import time
import email.mime.multipart
import email.mime.text
import traceback
pwd = "/usr/local/logtest/untitled2/logcenter/"

importantip=[]        ###将重要的报警IP提取出来
for line in open("%sip.txt" %pwd):
    importantip.append(line.replace('\n',''))

def sqloperate(data):
    if data == 'control':                          ###从数据库中读取赛选条件
        sql="select * from showlog_control order by power desc"
    elif data == 'discard':                         ###从数据库中读取过滤条件
        sql = "select * from showlog_discard"
    else:                                        ###从数据库中取出邮箱地址
        sql='SELECT emailaddress FROM showlog_user where groupname= "'+data+'" '
    return sqlreturn(sql)

def save(data,type):
    try:
        conn= pymysql.connect(host='localhost',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
        cur = conn.cursor()
        if type == 'historytable':
            for p in data:
                sql="INSERT INTO showlog_historytable(DATE,TIME,HOST)VALUES('"+str(p[0])+"','"+str(p[1].split('.')[0])+"','"+str(p[2])+"')"
                cur.execute(sql)
        elif type == 'table':
            for p in data:
                sql="INSERT INTO showlog_table(DATE,TIME,NAME,HOST,question,showmessage)VALUES('"+p[0]+"','"+p[1].split('.')[0]+"','"+p[2]+"','"+p[3]+"','"+p[4]+"','"+p[5]+"')"
                cur.execute(sql)
        cur.close()
        conn.commit()           ###利用事务来提高插入性能
        conn.close()
    except:
        sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")

def save_session(data):
    try:
        #sendmail2("1","traceback.print_exc():"+str(len(data)),"1","1","测试组")
        conn= pymysql.connect(host='10.90.10.102',
                              port = 3306,
                              user='root',
                              passwd='zpc123651085',
                              db ='logshow',
                              charset='utf8')
        cur = conn.cursor()
        sql = 'INSERT INTO showlog_sessiontable(DATE,TIME,HOST) VALUES(%s,%s,%s)' 
        param = [] 
        for p in data:
            param.append([p[0],p[1].split('.')[0],p[2]])
            # sql="INSERT INTO showlog_sessiontable(DATE,TIME,HOST)VALUES('"+data[p][0]+"','"+data[p][1].split('.')[0]+"','"+data[p][2]+"')"
        data.clear()
        cur.executemany(sql,param)
        cur.close()
        conn.commit()           ###利用事务来提高插入性能
        conn.close()
        param.clear()
    except:
        data.clear()
        sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
    #pass
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


def sendmail4(host,message,time,question,name):                         ###发送邮件函数
    fromaddr = "logcenter@alarm.ifeng.com"
    toaddr = "zhangpc1@ifeng.com"
    subject="[日志告警]"+host+" "+question+" "+str(time)
    message=message
    msg=email.mime.multipart.MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(email.mime.text.MIMEText(message))
    msg['From'] = fromaddr
    msg['To']= toaddr
    server = smtplib.SMTP('localhost')
    #server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()


def sendmail2(host,message,time,question,name):                         ###发送邮件函数
    server = smtplib.SMTP('localhost')
    fromaddr = "logcenter@alarm.ifeng.com"
    msg=email.mime.multipart.MIMEMultipart()
    msg.attach(email.mime.text.MIMEText(message))
    if question.strip()!='up' and question.strip()!='down':
        msg['Subject'] = "[日志告警]"+host+" "+question+" "+time
        for i in sqloperate(name):
            toaddr = i['emailaddress']
            server.sendmail(fromaddr, toaddr, msg.as_string())
    else:
        if host in importantip:
            msg['Subject'] = "[日志告警]"+host+" "+"端口up/down"+" "+time
            for i in sqloperate(name):
                toaddr = i['emailaddress']
                server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

def sendmail3(host,message,time,question,name):                         ###发送邮件函数
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
