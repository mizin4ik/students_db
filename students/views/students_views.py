# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Students

def student_list(request):
    students = (
        {
            'id': 1,
            'first_name': u'Вікторія',
            'last_name': u'Кіт',
            'ticket': 235,
            'image': 'img/pic1.jpg'
        },
        {
            'id': 2,
            'first_name': u'Софія',
            'last_name': u'Нельсон',
            'ticket': 2351,
            'image': 'img/pic2.jpg'
        },
        {
            'id': 3,
             'first_name': u'Клава',
             'last_name': u'Іванишин',
             'ticket': 329,
             'image': 'img/pic3.jpg'
        }
    )
    return render(request, 'students/students_list.html', {'students' : students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
