import subprocess
import time
import datetime
import smtplib
import logging
import email.mime.multipart    
import email.mime.text  
import os

def getresult():
    times=str(datetime.datetime.now())
    sendmail2(times,"进程停止了")
    os.system("python /usr/local/logtest/logchoose.py &")
    sendmail2(str(datetime.datetime.now()),"进程启动啦") 

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
    msg.attach(email.mime.text.MIMEText(message))
    smtp = smtplib.SMTP()
    smtp.connect(MAIL_HOST,25)
    smtp.login(MAIL_USER, MAIL_PWD)
    smtp.sendmail(MAIL_FROM,['447143800@qq.com'], msg.as_string())
    smtp.quit()

getresult() if 'logchoose.py' not in subprocess.getoutput("ps -ef|grep logchoose") else ""
#time.sleep(300)
