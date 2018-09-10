# -*- coding: utf-8 -*-
import imghdr

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView
from datetime import datetime

from ..models import Student, Group


# Views for Students

def student_list(request):
    students = Student.objects.all()

    #try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    # was form posted?
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = 'Ім’я є обов’язковим'
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = 'Прізвище є обов’язковим'
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = 'Дата народження є обов’язковою'
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = 'Введіть коректний формат дати(напр.1984-12-30)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = 'Білет є обов’язковим'
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = 'Оберіть групу для студента'
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = 'Оберіть коректну групу'
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                if imghdr.what(photo):
                    if photo.size <= 2097152:
                        data['photo'] = photo
                    else:
                        errors['photo'] = 'Розмір фото не повинен перевищувати 2мб'

                else:
                    errors['photo'] = 'Завантажте правильний формат фото'

            # save student

            if not errors:
                student = Student(**data)
                student.save()

                # redirect to students list
                messages.success(request, 'Студента "{0} {1}" успішно додано!'.format(first_name, last_name))

                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.info(request, 'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))

    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'notes', 'student_group')

    def get_success_url(self):
        messages.success(self.request, 'Редагування студента успішне!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Редагування студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
