# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Groups
def groups_list(request):
    groups = (
        {
            'id': 1,
            'name': u'Мтм-21',
            'leader': {'id': 1, 'name': u'Кіт Вікторія'}
        },
        {
            'id': 2,
            'name': u'Мтм-21',
            'leader': {'id': 2, 'name': u'Нельсон Софія'}
        },
        {
            'id': 3,
            'name': u'Мтм-21',
            'leader': {'id': 3, 'name': u'Іванишин Клава'}
        }
    )
    return render(request, 'students/group.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
