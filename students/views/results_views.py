# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from students.util import paginate
from ..models import Result


class ResultList(TemplateView):
    template_name = 'students/exam_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Result.objects.all()

        # try to order results list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('result', 'id'):
            results = results.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                results = results.reverse()
        else:
            results = results.order_by('result')

        # paginate result
        context = paginate(results, 10, self.request, context, var_name='results')
        return context


def results_add(request):
    return HttpResponse('<h1>Results add form</h1>')


def results_edit(request, res):
    return HttpResponse('<h1>Edit results {0}</h1>'.format(res))


def results_delete(request, res):
    return HttpResponse('<h1>Delete results {0}</h1>'.format(res))
