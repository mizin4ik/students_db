# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from students.util import paginate
from ..models import Exam


class ExamsList(TemplateView):
    template_name = 'students/exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exams = Exam.objects.all()

        # try to order exams list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('exams_name', 'exams_date', 'professor', 'id'):
            exams = exams.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                exams = exams.reverse()
        else:
            exams = exams.order_by('exams_date')

        # paginate exams
        context = paginate(exams, 10, self.request, context, var_name='exams')
        return context


def exams_add(request):
    return HttpResponse('<h1>Exams add form</h1>')


def exams_edit(request, exe):
    return HttpResponse('<h1>Edit exams {0}</h1>'.format(exe))


def exams_delete(request, exe):
    return HttpResponse('<h1>Delete exams {0}</h1>'.format(exe))
