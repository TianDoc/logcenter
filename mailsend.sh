#!/bin/bash
datetime=`date`
##echo "$datetime mailaddress:$1 sub:$2  con:$3 ">>/usr/lib/zabbix/alertscripts/mailalarm.log >/dev/null 2>&1 &
echo "$datetime mailaddress:$1 sub:$2  con:$3 ">>/usr/local/logtest/untitled2/logcenter/mailsend.log
subject=`echo "$2"|iconv -f utf-8   `
message=`echo "$3"|iconv -f utf-8 `
#subject=`echo "$2"
#message=`echo "$3"
#echo "$message"|mail -s "$subject" $1 -- -f "alarm@alarm.ifeng.com" >/dev/null 2>&1
echo "$message"|mail -r logcenter@alarm.ifeng.com -s "$subject" $1

