# -*- coding: utf-8 -*-
import imghdr

from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView

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


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'notes', 'student_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.add_input(Submit('add_button', 'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', 'Скасувати', css_class='btn btn-link'))


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'notes', 'student_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.add_input(Submit('add_button', 'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', 'Скасувати', css_class='btn btn-link'))


    def clean_photo(self):
        if self.cleaned_data.get('photo'):
            photo = self.cleaned_data.get('photo')
            photo_errors = []

            if imghdr.what(photo):
                if photo.size <= 2000000:
                    return photo
                else:
                    photo_errors.append('Розмір фото не повинен перевищувати 2мб')
            else:
                photo_errors.append('Завантажте правильний формат фото')

            self._errors['photo'] = photo_errors


class StudentCreateView(CreateView):
    model = Student
    template_name = 'students/students_add.html'
    form_class = StudentCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Додавання студента успішне!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Редагування студента успішне!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Редагування студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm-delete.html'

    def get_success_url(self):
        messages.success(self.request, ' Студента успішно видалено!')
        return reverse('home')