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
from django.urls import path, re_path

from students.views import StudentsList, StudentCreateView, StudentDeleteView, GroupsDeleteView, GroupCreateView, \
    GroupUpdateView, JournalView, GroupsList, ExamsList, ExamCreateView, ExamUpdateView, ExamDeleteView, ResultList

from students.views import results_add
from students.views import results_edit
from students.views import results_delete

from students.views import contact_admin

from students.views import StudentUpdateView


urlpatterns = [
    # Students url
    re_path(r'^$', StudentsList.as_view(), name="home"),
    re_path(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),
    re_path(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    re_path(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    # Groups url
    re_path(r'^groups/$', GroupsList.as_view(), name="groups"),
    re_path(r'^groups/add/$', GroupCreateView.as_view(), name='groups_add'),
    re_path(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    re_path(r'^groups/(?P<pk>\d+)/delete/$', GroupsDeleteView.as_view(), name='groups_delete'),

    # Visiting url
    re_path(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Exams url
    re_path(r'^exams/$', ExamsList.as_view(), name="exams"),
    re_path(r'^exams/add/$', ExamCreateView.as_view(), name='exams_add'),
    re_path(r'^exams/(?P<pk>\d+)/edit/$', ExamUpdateView.as_view(), name="exams_edit"),
    re_path(r'^exams/(?P<pk>\d+)/delete/$', ExamDeleteView.as_view(), name="exams_delete"),

    # Results url
    re_path(r'^results/$', ResultList.as_view(), name="results"),
    re_path(r'^results/add/$', results_add, name='results_add'),
    re_path(r'^results/(?P<res>\d+)/edit$', results_edit, name="results_edit"),
    re_path(r'^results/(?P<res>\d+)/delete$', results_delete, name="results_delete"),

    re_path(r'^contact-admin/$', contact_admin, name='contact_admin'),

    path('admin/', admin.site.urls),   
]

if DEBUG:
    # serve files from media folder urlpatterns += patterns(’’,
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
