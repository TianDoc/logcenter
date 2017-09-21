# coding=utf8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from .models import table
from .models import user
from .models import control
from .models import group
from .models import historytable
from django.utils.timezone import now, timedelta
import datetime
import time
from django.db.models import Q
from collections import OrderedDict
import random
from collections import deque
import json
from .operate import *
from .operate_table import *

def index(request):
    return render(request,"index.html")

def home(request):  ##主界面
    try:
        request.session['fastselect']=[]
        for line in open("/usr/local/logtest/untitled2/logcenter/fastselect.txt"):
            request.session['fastselect'].append(line.replace("\n",""))
    except:
        pass
    message,page,types,logal = gettable(request)
    return render(request, 'logshow.html', {'page':page,'message': message,'logal':logal,'type':types,'fastselect':request.session['fastselect']})
 
def controlget(request):  ##赛选条件界面
    controllist=control.objects.all()
    return render(request,'control.html',{'control':controllist})

def userget(request):  ##用户管理界面
    userlist=user.objects.all()
    return render(request,'user.html',{'user':userlist})

def groupget(request):  ##用户组管理界面
    grouplist=group.objects.all()
    return render(request,'group.html',{'group':grouplist})

def detail(request):        ##修改界面
    return change_change(request)

def turnback(request):      ##跳转界面
    return finish_change(request)

def showmessage(request):
    d,m,logal = draw_pie(request)
    return render(request, 'showmessage.html', {'d':d,'logal':logal,'number':m})

def historytablelist(request):
    if  'ip' in request.GET:
        return gethistorytable(request)
    return render(request, 'historytable.html',{'number':0})

def fastselect(request):
    return render(request,'fastselect.html',{'fastselect':request.session['fastselect']})

def newpassword(request):  ##日志种类管理界面
    if 'long' in request.GET:
        try:
            password=getnewpassword(int(request.GET['long']))
            return render(request,'logstyle.html',{'password':password})
        except:
            return render(request, 'logstyle.html')
    return render(request, 'logstyle.html')

def getnewpassword(a):
    password = ["a", "b", "c", "d", "e", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x",
                "y", "z", "1", "2", "3", "4", "5", "6",
                "7", "8", "9", "0", "#", "@", "!", ".",
                "+", "-", "*"]
    return "".join([password[random.randint(0, 42)] for m in range(a)])


# def timeturn(request):
#     if 'starttime' in request.GET:
#         return render(request, 'time.html',{'starttime':request.GET['starttime'],'endtime':request.GET['endtime']})
#     return render(request, 'time.html')
#     
# def setting(request):
#     if request.GET['ip']:
#         config={ "service": [
# {'zabbix':'/var/log/zabbix/zabbix_server.log'},{'httpd':'/var/log/httpd/access_log'}
# ]}
#         return HttpResponse(json.dumps(config))
#     config={ "service": [{'httpd':'/var/log/httpd/access_log'}]}
#     return HttpResponse(json.dumps(config))

# def testapi(request):
#     if 'hostip' in request.GET:
#         return render(request,'api.html',{'hostip':request.GET['hostip']})
#     if 'date' in request.GET:
        
#         return render(request,'api.html',{'hostip':request.GET['date']})
#     if 'zabbixlog' in request.POST:
#         line=[]
#         for i in request.POST['zabbixlog']:
#             line.append(i)
#         return render(request,'api.html',{'hostip':request.POST['zabbixlog']})
#         #return render(request,'api.html',{'hostip':line})
#     else:
#         return render(request,'api.html',{'hostip':"禁止"})
