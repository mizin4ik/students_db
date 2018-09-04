# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Result


def results_list(request):
    results = Result.objects.all()

    # try to order results list
    order_by = request.GET.get('order_by', '')
    if order_by in ('result', 'id'):
        results = results.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            results = results.reverse()
    else:
        results = results.order_by('result')

    # paginate result
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'students/exam_result.html', {'results': results})


def results_add(request):
    return HttpResponse('<h1>Results add form</h1>')


def results_edit(request, res):
    return HttpResponse('<h1>Edit results {0}</h1>'.format(res))


def results_delete(request, res):
    return HttpResponse('<h1>Delete results {0}</h1>'.format(res))
