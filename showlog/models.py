# Create your models here.
from django.db import models
import time
import datetime


# Create your models here.
class table(models.Model):
    date = models.TextField()
    name=models.CharField(max_length=30)
    question = models.CharField(max_length=30)
    host = models.CharField(max_length=30)
    time=models.IntegerField()
    id=models.IntegerField(primary_key=True)
    showmessage=models.CharField(max_length=50,null=True)

class control(models.Model):
    keyword=models.CharField(max_length=90)
    times=models.IntegerField()
    contactsid=models.IntegerField()
    contactsname=models.CharField(max_length=30)
    id=models.IntegerField(primary_key=True)
    nokeyword = models.TextField(null=True)
    showmessage = models.CharField(max_length=50, null=True)
    power=models.IntegerField(default=1)
    #usetag=models.IntegerField(default=1)    

class user(models.Model):
    user=models.CharField(max_length=30)
    telephone=models.CharField(max_length=30)
    emailaddress=models.CharField(max_length=30)
    id=models.IntegerField(primary_key=True)
    groupid=models.IntegerField()
    groupname=models.CharField(max_length=30)


class group(models.Model):
    groupname=models.CharField(max_length=30)
    id=models.IntegerField(primary_key=True)

class historytable(models.Model):
    date = models.TextField()
    host = models.CharField(max_length=30)
    time = models.IntegerField()
    id = models.IntegerField(primary_key=True)

class selected(models.Model):

    id = models.IntegerField(primary_key=True)

class discard(models.Model):
    id =models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=90)
