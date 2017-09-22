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

def gettable(request):
    types = 1
    if 'cut' in request.GET:
        if request.GET['cut']=='2':
            logal = "最近一周"
            timequit = int(time.time())-7*24*60*60
            message = table.objects.filter(time__gt=timequit).order_by('-time')
        elif request.GET['cut']=='3':
            logal = "最近一月"
            timequit = int(time.time())-30*24*60*60
            message = table.objects.filter(time__gt=timequit).order_by('-time')
        elif request.GET['cut']=='4':
            logal = "显示全部"
            message=table.objects.all().order_by('-time')
        elif request.GET['cut']=='1':
            logal = "最近一天"
            timequit = int(time.time())-1*24*60*60
            message = table.objects.filter(time__gt=timequit).order_by('-time')
        elif request.GET['cut']=='5':
            logal="历史纪录"
            types = 0
            message=table.objects.filter(date=table.objects.filter(id=request.GET['id'])[0].date).order_by('-time')
        elif request.GET['cut'] in request.session['fastselect']:
            logal = "显示" + request.GET['cut']
            message = table.objects.filter(question=request.GET['cut']).order_by('-time')
    else:
        logal = "最近一天"
        timequit = int(time.time())-1*24*60*60
        message = table.objects.filter(time__gt=timequit).order_by('-time')
    message,page = changetable(request,message)
    return message,page,types,logal

def changetable(request,message):
    page=GetPage(request,message)
    if  message:
        for i in range(len(message)):
            message[i].time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(message[i].time+8*60*60))
            if message[i].showmessage==None :
                 message[i].showmessage = control.objects.filter(keyword=message[i].question)[0].showmessage
        message = message[500 * (page['selectpage']-1):500 * page['selectpage'] ]
    return message,page

def gethistorytable(request):
    if request.GET['timequit']=="1" and (request.GET['starttime']=='' or request.GET['endtime']==''):
        timequit=time.time()-60*60*24*1
        history=historytable.objects.filter(Q(host=request.GET['ip'].strip())&Q(time__gt=timequit)).order_by('-time')
        select=1
    elif request.GET['timequit']=="2" and (request.GET['starttime']=='' or request.GET['endtime']==''):
        timequit=time.time()-60*60*24*3
        history = historytable.objects.filter(Q(host=request.GET['ip'].strip()) & Q(time__gt=timequit)).order_by('-time')
        select=2
    elif request.GET['timequit']=="3" and (request.GET['starttime']=='' or request.GET['endtime']==''):
        timequit=time.time()-60*60*24*7
        history = historytable.objects.filter(Q(host=request.GET['ip'].strip()) & Q(time__gt=timequit)).order_by('-time')
        select=3
    elif request.GET['starttime']!='' and request.GET['endtime']!='' : 
        starttime = time.mktime(time.strptime(request.GET['starttime'], "%Y-%m-%d %H:%M:%S"))-8*60*60
        endtime=time.mktime(time.strptime(request.GET['endtime'], "%Y-%m-%d %H:%M:%S"))-8*60*60
        history = historytable.objects.filter(Q(host=request.GET['ip'].strip()) & Q(time__gt=starttime)&Q(time__lt=endtime)).order_by('-time')
        history,page = changehistorytable(request,history)
        return render(request, 'historytable.html',{'page':page,'starttime':request.GET['starttime'],'endtime':request.GET['endtime'],'historytable': history, 'ip': request.GET['ip']})
    history,page = changehistorytable(request,history)
    return render(request, 'historytable.html',{'page':page,'select':select,'historytable':history,'ip':request.GET['ip']})

def changehistorytable(request,history):
    page = GetPage(request, history)
    if history:
        for i in range(len(history)):
            history[i].time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(history[i].time+8*60*60))
        history = history[500 * (page['selectpage'] - 1):500 * page['selectpage']]
    return history,page

def draw_pie(request):
    if 'cut' in request.GET:
        if request.GET['cut']=='1':
            logal = '显示一周'
            timequit = 60 * 60 * 24 * 7
        elif request.GET['cut']=='2':
            logal = '显示一月'
            timequit = 60 * 60 * 24 * 30
        elif request.GET['cut']=='3':
            logal = '显示全部'
            timequit = 0
    else:
        logal='显示一周'
        timequit = 60 * 60 * 24 * 7
    d,m=GetPie(timequit)
    if d['judgement'] == 1:
        del d['judgement']
    return d,m,logal

def GetPie(timesplit):  # @NoSelf
    d=OrderedDict()
    if not timesplit:
        m=len(table.objects.all())
        if m !=0:
            for a in control.objects.all():
                d[a.keyword]=[len(table.objects.filter(question=a.keyword))/m,'#'+hex(int(random.uniform(0.5,1)*16777215)).replace('0x','',1)]
            d['judgement']=1
            return d,m
        d['judgement']=0
        return d,m
    else:
        timequit=time.time()-timesplit
        m = len(table.objects.filter(time__gt=timequit))
        if m!=0:
            for a in control.objects.all():
                d[a.keyword]=[len(table.objects.filter(Q(question=a.keyword)&Q(time__gt=timequit)))/m,'#'+hex(int(random.uniform(0.5,1)*16777215)).replace('0x','',1)]
            d['judgement']=1
            return d,m
        d['judgement']=0
        return d,m

def GetPage(request,table):
    m={}
    number=len(table)
    page = int(number / 500) + 1
    if 'page' not in request.GET:
        selectpage=1
        pages=1
        if page > 10:
            pagelist = [x for x in range(1, 11)]
        else:
            pagelist = [x for x in range(1, page+1)]
    else:
        selectpage=int(request.GET['page'])
        if page > 10 :
            if selectpage > 5 and selectpage < (page - 5):
                pagelist = [x for x in range(int(request.GET['page'])-5, int(request.GET['page'])+5)]
            elif selectpage <= 5:
                pagelist = [x for x in range(1, 11)]
            elif selectpage >= (page - 5):
                pagelist = [x for x in range(page-9,page+1)]
        else:
            pagelist=[x for x in range(1,page+1)]
    m['tailpage'] = pagelist[-1]
    m['selectpage'] = selectpage
    m['endpage'] = page
    m['headpage']= 1
    m['page'] =pagelist
    m['number'] = number
    m['type']=GetType(request)
    return m

def GetType(request):
    if 'cut' in request.GET:
        if 'id' in request.GET:
            m = '&cut='+request.GET['cut']+'&id='+request.GET['id']
        else:
            m = '&cut=' + request.GET['cut']
    elif 'ip' in request.GET:
        m = '&ip='+request.GET['ip']+'&timequit='+request.GET['timequit']+'&starttime='+request.GET['starttime']+'&endtime='+request.GET['endtime']
    else:
        m = ''
    return m