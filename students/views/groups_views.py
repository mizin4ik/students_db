# -*- coding: utf-8 -*-
from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views.generic import DeleteView

from ..models import Group


def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader', 'id'):
        if order_by == 'leader':
            order_by = 'leader__first_name'
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')

    # paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/group.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


class GroupsDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm-delete.html'

    def get_success_url(self):
        messages.success(self.request, ' Групу успішно видалено!')
        return reverse('groups')
