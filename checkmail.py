import subprocess
import time
import datetime
import smtplib
import logging
import email.mime.multipart    
import email.mime.text  
import os
import traceback
def getresult():
    times=str(datetime.datetime.now())
    #sendmail2(times,"进程停止了")
    subprocess.getoutput("service sendmail restart")
    #sendmail2(str(datetime.datetime.now()),"进程启动啦") if 'logchoose.py' not in subprocess.getoutput("ps -ef|grep logchoose") else sendmail2(str(datetime.datetime.now()),"进程重启失败")

def getresult2():
    times = str(datetime.datetime.now())
    #sendmail2(times,"logstash停止了")
    os.system("logstash -f /usr/local/logstash-5.4.0/config/logstash_to_redis.conf &")
    sendmail2(times,"logstash停止了")
def sendmail2(times,message):
    MAIL_HOST = "smtp.126.com"
    MAIL_USER = "z550665887"
    MAIL_FROM = "z550665887@126.com"
    MAIL_PWD = "zpc159357"
    subject =times+message
    msg=email.mime.multipart.MIMEMultipart() 
    msg['From'] = MAIL_FROM
    msg['Subject'] = subject
    msg['To'] = "447143800@qq.com" 
    msg.attach(email.mime.text.MIMEText("邮件进程停止啦"))
    smtp = smtplib.SMTP()
    smtp.connect(MAIL_HOST,25)
    smtp.login(MAIL_USER, MAIL_PWD)
    smtp.sendmail(MAIL_FROM,['447143800@qq.com'], msg.as_string())
    smtp.quit()

while True:
    #print(subprocess.getoutput("ps -ef|grep sendmail"))
    try:
        getresult() if 'accepting connections' not in subprocess.getoutput("ps -ef|grep sendmail") else ""
        getresult2() if subprocess.getoutput("netstat -ntlp|grep :::2514") else ""
    except:
        sendmail2(str(datetime.datetime.now()),trackbace.format_exc())
    time.sleep(10)
