#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import paramiko
import operate
import traceback

"""
Ping 服务器功能
"""
def ping(ip):
    ping = os.system("ping -c 3 -W 3 %s" % (ip))
    return ping


def run(ip):

    today = time.strftime("%Y%m%d", time.localtime())

    if ping(ip):
        # 判断是否Ping通,3:未PING通
        operate.sendmail2("1",ip+"无法重启 ，原因ping不通"+today,"1","1","测试组")
    else:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        usr = 'autoac'
        psw = 'JT1VD54Gu8K9xKze'

        try:
            ssh.connect(ip, 22, usr, psw, allow_agent=False, look_for_keys=False)
            # setStatus(cur, conn, 4, ip, today)
            channel = ssh.invoke_shell()
            channel.settimeout(5)

            # channel.send('screen-length disable')
            # channel.send('\n')
            # channel.send('dis cu')
            # channel.send('\n')

            # buff = ''
            # while not buff.endswith('>'):
            #     time.sleep(2)
            #     resp = channel.recv(9999)
            #     buff += resp

            # confArr = buff.split('\r\n')
            # for line in confArr:
            #     if line != '' and '<' + hostName + '>' not in line and '% Screen-length ' not in line:
            #         confText += line + '\r\n'

            # dir = fileSave(hostName, confText)
            # dirSql = "UPDATE `SwitchBackup` SET `status` = %d , `brand` = '%s', `dir` = '%s'  WHERE `host` = '%s' AND `day` = '%s'" % (
            # 1, brand, dir, ip, today)
            # exeUpdate(cur, conn, dirSql)

        except :
            operate.sendmail2("1","traceback.print_exc():"+traceback.format_exc(),"1","1","测试组")
        ssh.close()


