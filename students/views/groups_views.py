# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView, CreateView, UpdateView, TemplateView

from students.util import paginate
from ..models import Group


class GroupsList(TemplateView):
    template_name = 'students/group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        groups = Group.objects.all()

        # try to order groups list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title', 'leader', 'id'):
            if order_by == 'leader':
                order_by = 'leader__first_name'
            groups = groups.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                groups = groups.reverse()
        else:
            groups = groups.order_by('title')

        context = paginate(groups, 10, self.request, context, var_name='groups')
        return context


class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'leader', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
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


class GroupCreateView(CreateView):
    model = Group
    template_name = 'students/groups_add.html'
    form_class = GroupCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Додавання групи успішне!')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Додавання групи скасовано!')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super().post(request, *args, **kwargs)


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'leader', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
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

    def clean_leader(self):
        leader = self.cleaned_data.get('leader')

        if leader.group is self.instance or not leader.group:
            return leader
        self._errors['leader'] = ('Студент не належить даній групі',)


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Редагування групи успішне!')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Редагування групи скасовано!')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super().post(request, *args, **kwargs)


class GroupsDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm-delete.html'

    def get_success_url(self):
        return reverse('groups')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Групу успішно видалено!')
        except ProtectedError:
            messages.error(self.request, 'fffff')
            return HttpResponseRedirect(reverse('groups'))

        return HttpResponseRedirect(success_url)
