from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super().__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', 'Надіслати'))

    from_email = forms.EmailField(
        label="Ваша Емейл Адреса",
    )

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128,
    )

    message = forms.CharField(
        label=u"Текст повідомлення",
        widget=forms.Textarea,
    )
