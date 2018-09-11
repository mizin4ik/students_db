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

from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from students.views import student_list, StudentCreateView, StudentDeleteView, GroupsDeleteView

from students.views import groups_list
from students.views import groups_add
from students.views import groups_edit

from students.views import exams_list
from students.views import exams_add
from students.views import exams_edit
from students.views import exams_delete

from students.views import results_list
from students.views import results_add
from students.views import results_edit
from students.views import results_delete

from students.views import contact_admin

from students.views import visitor_list

from students.views import StudentUpdateView


urlpatterns = [
    # Students url
    re_path(r'^$', student_list, name="home"),
    re_path(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),
    re_path(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    re_path(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    # Groups url
    re_path(r'^groups/$', groups_list, name="groups"),
    re_path(r'^groups/add/$', groups_add, name='groups_add'),
    re_path(r'^groups/(?P<gid>\d+)/edit$', groups_edit, name="groups_edit"),
    re_path(r'^groups/(?P<pk>\d+)/delete/$', GroupsDeleteView.as_view(), name='groups_delete'),

    # Visiting url
    re_path(r'^visiting/$', visitor_list, name="visiting"),

    # Exams url
    re_path(r'^exams/$', exams_list, name="exams"),
    re_path(r'^exams/add/$', exams_add, name='exams_add'),
    re_path(r'^exams/(?P<exe>\d+)/edit$', exams_edit, name="exams_edit"),
    re_path(r'^exams/(?P<exe>\d+)/delete$', exams_delete, name="exams_delete"),

    # Results url
    re_path(r'^results/$', results_list, name="results"),
    re_path(r'^results/add/$', results_add, name='results_add'),
    re_path(r'^results/(?P<res>\d+)/edit$', results_edit, name="results_edit"),
    re_path(r'^results/(?P<res>\d+)/delete$', results_delete, name="results_delete"),

    re_path(r'^contact-admin/$', contact_admin, name='contact_admin'),

    path('admin/', admin.site.urls),   
]

if DEBUG:
    # serve files from media folder urlpatterns += patterns(’’,
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
