import pymysql
import pymysql.cursors
import smtplib
import os

pwd = "/usr/local/logtest/untitled2/logcenter/"

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
        for p in data:
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