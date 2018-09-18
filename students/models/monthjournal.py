from django.db import models


class MonthJournal(models.Model):
    class Meta:
        verbose_name = 'Місячний Журнал'
        verbose_name_plural = 'Місячні Журнали'

    student = models.ForeignKey(
        'Student',
        verbose_name='Студент',
        blank=False,
        unique_for_month='date',
        on_delete=models.PROTECT)

    date = models.DateField(
        verbose_name='Дата',
        blank=False)

    def __unicode__(self):
        return ' % s: % d, % d' % (self.student.last_name, self.date.month, self.date.year)


for i in range(1, 32):
    MonthJournal.add_to_class('present_day{0}'.format(i), models.BooleanField(default=False, null=True))
