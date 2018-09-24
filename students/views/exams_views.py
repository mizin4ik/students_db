# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from students.util import paginate, get_current_group
from ..models import Exam


class ExamsList(TemplateView):
    template_name = 'students/exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_group = get_current_group(self.request)
        if current_group:
            exams = Exam.objects.filter(exams_group=current_group)
        else:
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


class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ('exams_name', 'exams_date', 'professor', 'exams_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('exams_add')
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


class ExamCreateView(CreateView):
    model = Exam
    template_name = 'students/exams_add.html'
    form_class = ExamCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Додавання іспиту успішне!')
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Додавання групи скасовано!')
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super().post(request, *args, **kwargs)


class ExamUpdateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ('exams_name', 'exams_date', 'professor', 'exams_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('exams_edit', kwargs={'pk': kwargs['instance'].id})
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


class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/exams_edit.html'
    form_class = ExamUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Редагування іспиту успішне!')
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Редагування іспиту скасовано!')
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super().post(request, *args, **kwargs)


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm-delete.html'

    def get_success_url(self):
        return reverse('exams')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Іспит успішно видалено!')
        except ProtectedError:
            messages.error(self.request, 'fffff')
            return HttpResponseRedirect(reverse('results'))

        return HttpResponseRedirect(success_url)
