"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from showlog import views as showlog_views  # @UnresolvedImport

urlpatterns = [
    url(r'^index', showlog_views.index,name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^logshow', showlog_views.home,name="logshow"),
    url(r'^user', showlog_views.userget,name="userlist"),
    url(r'^control', showlog_views.controlget,name="controllist"),
    url(r'^group', showlog_views.groupget,name="grouplist"),
    url(r'^newpassword', showlog_views.newpassword,name="newpasswordget"),
    url(r'^detail', showlog_views.detail, name="detail"),
    url(r'^turnback', showlog_views.turnback, name="turnback"),
    url(r'^showmessage', showlog_views.showmessage, name="showmessage"),
    url(r'^historytable', showlog_views.historytablelist, name="historytable"),
    url(r'^fastselect', showlog_views.fastselect, name="fastselect"),
    # url(r'^timeturn', showlog_views.timeturn, name="timeturn"),
    # url(r'^test/api',showlog_views.testapi),
    # url(r'^test/setting',showlog_views.setting),
]
