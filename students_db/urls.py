"""students_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from students.views import student_list
from students.views import students_add
from students.views import students_edit
from students.views import students_delete

from students.views import groups_list
from students.views import groups_add
from students.views import groups_edit
from students.views import groups_delete

from students.views import visitor_list


urlpatterns = [
    # Students url
    re_path(r'^$', student_list, name="home"),
    re_path(r'^students/add/$', students_add, name='students_add'),
    re_path(r'^students/(?P<sid>\d+)/edit$', students_edit, name="students_edit"),
    re_path(r'^students/(?P<sid>\d+)/delete$', students_delete, name="students_delete"),

    # Groups url
    re_path(r'^groups/$', groups_list, name="groups"),
    re_path(r'^groups/add/$', groups_add, name='groups_add'),
    re_path(r'^groups/(?P<gid>\d+)/edit$', groups_edit, name="groups_edit"),
    re_path(r'^groups/(?P<gid>\d+)/delete$', groups_delete, name="groups_delete"),

    # Visiting url
    re_path(r'^visiting/$', visitor_list, name="visiting"),

    path('admin/', admin.site.urls),   
]
