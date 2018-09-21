# -*- coding: utf-8 -*-
import imghdr


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView

from students.util import paginate, get_current_group
from ..models import Student


# Views for Students

class StudentsList(TemplateView):
    template_name = 'students/students_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_group = get_current_group(self.request)
        if current_group:
            students = Student.objects.filter(student_group=current_group)
        else:
            students = Student.objects.all()

        # try to order students list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'ticket', 'id'):
            students = students.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                students = students.reverse()
        else:
            students = students.order_by('last_name')

        context = paginate(students, 10, self.request, context, var_name='students')
        return context


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