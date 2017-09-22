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

def change_change(request):
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
    elif request.GET['type']=='4':                 #####删除快捷选项
        lines = []
        for line in open("/usr/local/logtest/untitled2/logcenter/fastselect.txt"):
            if line.replace('\n','') != request.GET['id']:
                lines.append(line)
        f = open("/usr/local/logtest/untitled2/logcenter/fastselect.txt", 'w')  ##覆盖读写
        for i in lines:
            f.write(i)
        f.close()
        request.session['fastselect']=lines
        return render(request, 'fastselect.html', {'fastselect':lines})
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
    elif request.GET['type']=='24':
        request.session['type'] = request.GET['type']
        return render(request, 'detail.html')

def finish_change(request):
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
    elif request.session['type']=='24':
        if request.GET['fastselect'] not in request.session['fastselect']:
            f = open("/usr/local/logtest/untitled2/logcenter/fastselect.txt", 'a')
            f.write(request.GET['fastselect']+'\n')
            f.close()
            request.session['fastselect'] = []
            for line in open("/usr/local/logtest/untitled2/logcenter/fastselect.txt"):
                request.session['fastselect'].append(line.replace("\n", ""))
        return render(request, 'fastselect.html', {'fastselect': request.session['fastselect']})

def checktext(text):            ##判断屏蔽字格式是否正确
    if text=="":
        return ""
    if "" in [x.strip() for x in text.split(',')]:
        return 0
    else:
        return ",".join([x.strip() for x in text.split(',')])