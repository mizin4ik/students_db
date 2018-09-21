from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from django.views.generic import TemplateView

from students.models import MonthJournal, Student
from ..util import paginate, get_current_group

from django.http import JsonResponse


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        current_group = get_current_group(self.request)
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        context['cur_month'] = month.strftime('%Y-%m-%d')

        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d, 'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days + 1)]

        if kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        elif current_group:
            queryset = Student.objects.filter(student_group=current_group)
        else:
            queryset = Student.objects.order_by('last_name')

        update_url = reverse('journal')

        students = []

        for student in queryset:
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception as err:
                print(err)
                journal = None

            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day{0}'.format(day), False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'), })

            students.append({
                'fullname': ' % s % s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context = paginate(students, 10, self.request, context, var_name='students')
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = bool(data['present'])
        student = Student.objects.get(pk=data['pk'])

        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        setattr(journal, 'present_day{0}'.format(current_date.day), present)
        journal.save()

        return JsonResponse({'status': 'success'})
