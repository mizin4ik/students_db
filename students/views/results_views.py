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


class ResultCreateForm(ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'exam', 'result')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('results_add')
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


class ResultCreateView(CreateView):
    model = Result
    template_name = 'students/results_add.html'
    form_class = ResultCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Додавання результату іспиту успішне!')
        return reverse('results')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Додавання результату іспиту скасовано!')
            return HttpResponseRedirect(reverse('results'))
        else:
            return super().post(request, *args, **kwargs)


class ResultUpdateForm(ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'exam', 'result')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('results_edit', kwargs={'pk': kwargs['instance'].id})
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


class ResultUpdateView(UpdateView):
    model = Result
    template_name = 'students/results_edit.html'
    form_class = ResultUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Редагування результату іспиту успішне!')
        return reverse('results')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Редагування результату іспиту скасовано!')
            return HttpResponseRedirect(reverse('results'))
        else:
            return super().post(request, *args, **kwargs)


class ResultDeleteView(DeleteView):
    model = Result
    template_name = 'students/results_confirm-delete.html'

    def get_success_url(self):
        return reverse('results')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Результат іспиту успішно видалено!')
        except ProtectedError:
            messages.error(self.request, 'fffff')
            return HttpResponseRedirect(reverse('results'))

        return HttpResponseRedirect(success_url)
