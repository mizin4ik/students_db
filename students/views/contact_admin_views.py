from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from students_db.local_settings import ADMIN_EMAIL
from students.models.contact_admin_models import ContactForm


def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                messages.error(request, 'Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше.')

            else:
                messages.success(request, 'Повідомлення успішно надіслане!')

            # redirect to same contact page with success message
            return render(request, 'students/contact_admin/form.html', {'form': form})

        else:
            messages.error(request, 'Будь-ласка, виправте наступні помилки')

        return render(request, 'students/contact_admin/form.html', {'form': form})


    # if there was not POST render blank form
    else:
        form = ContactForm()
        return render(request, 'students/contact_admin/form.html', {'form': form})