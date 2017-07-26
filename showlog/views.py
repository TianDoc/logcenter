
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

def home(request):  ##主界面
    if 'cut' in request.GET:
        if request.GET['cut']=='2':
            logal = "最近一周"
            timequit=int(time.mktime((datetime.datetime.now()- datetime.timedelta(days = 7)).timetuple()))
            message = table.objects.filter(time__gt=timequit)
            if  message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage               
            return render(request, 'logshow.html', {'message': message,'logal':logal,'type':1})
        elif request.GET['cut']=='3':
            logal = "最近一月"
            timequit = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple()))
            message = table.objects.filter(time__gt=timequit)
            if  message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage                   
            return render(request, 'logshow.html', {'message': message,'logal':logal,'type':1})
        elif request.GET['cut']=='4':
            logal = "显示全部"
            message=table.objects.all().order_by('time')
            if  message :
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage                 
            return render(request, 'logshow.html', {'message': message[::-1],'logal':logal,'type':2})
        elif request.GET['cut']=='1':
            logal = "最近一天"
            timequit = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))
            message = table.objects.filter(time__gt=timequit)
            if  message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage
            return render(request, 'logshow.html', {'message': message,'logal':logal,'type':1})
        elif request.GET['cut']=='5':    
            message=table.objects.filter(date=table.objects.filter(id=request.GET['id'])[0].date)
            logal="历史纪录"
            if message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage
            return render(request, 'logshow.html', {'message': message[::-1], 'logal': logal, 'type': 3})
        elif request.GET['cut']=='OSPFV2':
            logal = "显示OSPFV2"
            message = table.objects.filter(question="ospf")
            if message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage
            return render(request, 'logshow.html', {'message': message, 'logal': logal, 'type': 1})
        elif request.GET['cut']=='up/down':
            logal = "显示up/down"
            message = table.objects.filter(Q(question="up")|Q(question="down"))
            if message:
                for i in range(len(message)):
                    message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
                    if message[i].showmessage==None :
                         message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage                   
            return render(request, 'logshow.html', {'message': message, 'logal': logal, 'type': 1})
    logal="最近一天"
    timequit = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))
    message = table.objects.filter(time__gt=timequit)
    if  message:
        for i in range(len(message)):
            message[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(message[i].time+8*60*60))
            if message[i].showmessage==None :
                message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage 
    return render(request, 'logshow.html', {'message': message,'logal':logal,'type':1})

def controlget(request):  ##赛选条件界面
    controllist=control.objects.all()
    return render(request,'control.html',{'control':controllist})

def userget(request):  ##用户管理界面
    userlist=user.objects.all()
    return render(request,'user.html',{'user':userlist})

def groupget(request):  ##用户组管理界面
    grouplist=group.objects.all()
    return render(request,'group.html',{'group':grouplist})

def newpassword(request):  ##日志种类管理界面
    if 'long' in request.GET:
        password=getnewpassword(int(request.GET['long']))
        return render(request,'logstyle.html',{'password':password})
    return render(request, 'logstyle.html')

def detail(request):        ##修改界面
    if request.GET['type']=='1':                    ####删除联系人小组
        if group.objects.filter(id=int(request.GET['id'])):
            user.objects.filter(groupid=request.GET['id']).update(groupid=0,groupname="")
            control.objects.filter(contactsid=request.GET['id']).update(contactsid=0,contactsname="")
            group.objects.get(id=int(request.GET['id'])).delete()
        grouplist = group.objects.all()
        return render(request, 'group.html', {'group': grouplist})
    elif request.GET['type']=='2':                 #####删除联系人
        user.objects.get(id=int(request.GET['id'])).delete() if user.objects.filter(id=int(request.GET['id'])) else ""
        userlist = user.objects.all()
        return render(request, 'user.html', {'user': userlist})
    elif request.GET['type']=='3':                 #####删除筛选条件
        control.objects.get(id=int(request.GET['id'])).delete() if control.objects.filter(id=int(request.GET['id'])) else ""
        controllist = control.objects.all()
        return render(request, 'control.html', {'control': controllist})
    elif request.GET['type']=='11':                 ####联系小组修改
        request.session['id']=int(request.GET['id'])
        request.session['type']=request.GET['type']
        grouplist=group.objects.filter(id=int(request.GET['id']))
        return render(request, 'detail.html', {'group': grouplist[0]})
    elif request.GET['type']=='12':                 ####联系人修改
        request.session['id'] = int(request.GET['id'])
        request.session['type'] = request.GET['type']
        userlist = user.objects.filter(id=int(request.GET['id']))
        grouplist = group.objects.all()
        return render(request, 'detail.html', {'user': userlist[0],'group':grouplist})
    elif request.GET['type']=='13':                 ####筛选条件修改
        request.session['id'] = int(request.GET['id'])
        request.session['type'] = request.GET['type']
        controllist=control.objects.filter(id=int(request.GET['id']))
        grouplist = group.objects.all()
        return render(request, 'detail.html', {'control': controllist[0],'group':grouplist})
    elif request.GET['type']=='21' or request.GET['type']=='22' or request.GET['type']=='23':
        request.session['type'] = request.GET['type']
        grouplist = group.objects.all()
        return render(request, 'detail.html', { 'group': grouplist})

def turnback(request):      ##跳转界面
    if request.session['type']=='11':                ####联系小组修改
        group.objects.filter(id=int(request.session['id'])).update(groupname=request.GET['groupname'])
        user.objects.filter(groupid=int(request.session['id'])).update(groupname=request.GET['groupname'])
        control.objects.filter(contactsid=int(request.session['id'])).update(contactsname=request.GET['groupname'])
        grouplist = group.objects.all()
        return render(request, 'group.html', {'group': grouplist})
    elif request.session['type']=='12':              ####联系人修改
        user.objects.filter(id=int(request.session['id'])).update(user=request.GET['user'],
                                                                  telephone=request.GET['telephone'],
                                                                  emailaddress=request.GET['emailaddress'],
                                                                  groupname=request.GET['groupselect'],
                                                                  groupid=group.objects.filter(groupname=request.GET['groupselect'])[0].id)
        userlist = user.objects.all()
        return render(request, 'user.html', {'user': userlist})
    elif request.session['type']=='13':              ####筛选条件修改
        if checktext(request.GET['nokeyword']) != 0:
            control.objects.filter(id=int(request.session['id'])).update(keyword=request.GET['keyword'],
                                                                         times=request.GET['times'],
                                                                         contactsname=request.GET['groupselect'],
                                                                         nokeyword=checktext(request.GET['nokeyword']),
                                                                         showmessage=request.GET['showmessage'],
                                                                         contactsid=group.objects.filter(groupname=request.GET['groupselect'])[0].id,
                                                                         power=int(request.GET['power']))
        controllist = control.objects.all()
        return render(request, 'control.html', {'control': controllist})
    elif request.session['type']=='21':              ####新建联系人小组
        group.objects.create(groupname=request.GET['groupname']) if not group.objects.filter(groupname=request.GET['groupname'])  else ""
        grouplist = group.objects.all()
        return render(request, 'group.html', {'group': grouplist})
    elif request.session['type']=='22':              ####新建联系人
        user.objects.create(user=request.GET['user'],telephone=request.GET['telephone'],
                            emailaddress=request.GET['emailaddress'],groupname=request.GET['groupselect'],
                            groupid=group.objects.get(groupname=request.GET['groupselect']).id) if not user.objects.filter(user=request.GET['user']) else ""
        userlist = user.objects.all()
        return render(request, 'user.html', {'user': userlist})
    elif request.session['type']=='23':               ####新建筛选条件
        if checktext(request.GET['nokeyword']) !=0:   ####判断用户的屏蔽字格式是否正确
            control.objects.create(keyword=request.GET['keyword'],times=request.GET['times'],
                                   showmessage=request.GET['showmessage'],contactsname=request.GET['groupselect'],
                                   contactsid=group.objects.get(groupname=request.GET['groupselect']).id,
                                   nokeyword=checktext(request.GET['nokeyword']),
                                   power=int(request.GET['power'])) if not control.objects.filter(keyword=request.GET['keyword']) else ""
        controllist = control.objects.all()
        return render(request, 'control.html', {'control': controllist})

def showmessage(request):
    if 'cut' in request.GET:
        if request.GET['cut']=='1':
            logal = '显示一周'
            d = getpie(60 * 60 * 24 * 7)
            if d['judgement']==1:
                del d['judgement']
            return render(request, 'showmessage.html', {'d': d, 'logal': logal})
        elif request.GET['cut']=='2':
            logal = '显示一月'
            d = getpie(60 * 60 * 24 * 30)
            if d['judgement']==1:
                del d['judgement']
            return render(request, 'showmessage.html', {'d': d, 'logal': logal})
        elif request.GET['cut']=='3':
            logal = '显示全部'
            d = getpie(0)
            if d['judgement']==1:
                del d['judgement']
            return render(request, 'showmessage.html', {'d': d, 'logal': logal})
    logal='显示一周'
    d=getpie(60*60*24*7)
    if d['judgement'] == 1:
        del d['judgement']
    return render(request, 'showmessage.html', {'d':d,'logal':logal})

def historytable(request):
    if 'timequit' in request.GET and 'ip' in request.GET:
        if request.GET['timequit']=="1":
            timequit=time.time()-60*60*24
            history=historytable.objects.filter(Q(host=request.GET['ip'])&Q(time__gt=timequit))
            if history:
                for i in range(len(history)):
                    history[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(history[i].time+8*60*60))
            return render(request, 'historytable.html',{'select':'1','historytable':history,'ip':request.GET['ip']})
        elif request.GET['timequit']=="2":
            timequit = time.time()-60*60*24*3
            history = historytable.objects.filter(Q(host=request.GET['ip']) & Q(time__gt=timequit))
            if history:
                for i in range(len(history)):
                    history[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(history[i].time+8*60*60))
            return render(request, 'historytable.html',{'select': '2', 'historytable': history, 'ip': request.GET['ip']})
        elif request.GET['timequit']=="3":
            timequit = time.time()-60*60*24*7
            history = historytable.objects.filter(Q(host=request.GET['ip']) & Q(time__gt=timequit))
            if history:
                for i in range(len(history)):
                    history[i].time = time.strftime("%Y %b %d %H:%M:%S", time.localtime(history[i].time+8*60*60))
            return render(request, 'historytable.html',{'select': '3', 'historytable': history, 'ip': request.GET['ip']})
    return render(request, 'historytable.html')


def checktext(text): 			##判断屏蔽字格式是否正确
    if text=="":
        return ""
    if "" in [x.strip() for x in text.split(',')]:
        return 0
    else:
        return ",".join([x.strip() for x in text.split(',')])

def getpie(timesplit):  # @NoSelf
    d=OrderedDict()
    if timesplit==0:
        m=len(table.objects.all())
        if m !=0:
            for a in control.objects.all():
                d[a.keyword]=[len(table.objects.filter(question=a.keyword))/m,'#'+hex(int(random.uniform(0.5,1)*16777215)).replace('0x','',1)]
            d['judgement']=1
            return d
        d['judgement']=0
        return d
    else:
        timequit=time.time()-timesplit
        m = len(table.objects.filter(time__gt=timequit))
        if m!=0:
            for a in control.objects.all():
                d[a.keyword]=[len(table.objects.filter(Q(question=a.keyword)&Q(time__gt=timequit)))/m,'#'+hex(int(random.uniform(0.5,1)*16777215)).replace('0x','',1)]
            d['judgement']=1
            return d
        d['judgement']=0
        return d

def getnewpassword(a):
    password = ["a", "b", "c", "d", "e", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x",
                "y", "z", "1", "2", "3", "4", "5", "6",
                "7", "8", "9", "0", "#", "@", "!", ".",
                "+", "-", "*"]
    return "".join([password[random.randint(0, 42)] for m in range(a)])

