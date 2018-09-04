# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Exam


def exams_list(request):
    exams = Exam.objects.all()

    # try to order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('exams_name', 'exams_date', 'professor', 'id'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('exams_date')

    # paginate exams
    paginator = Paginator(exams, 3)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams.html', {'exams': exams})


def exams_add(request):
    return HttpResponse('<h1>Exams add form</h1>')


def exams_edit(request, exe):
    return HttpResponse('<h1>Edit exams {0}</h1>'.format(exe))


def exams_delete(request, exe):
    return HttpResponse('<h1>Delete exams {0}</h1>'.format(exe))
