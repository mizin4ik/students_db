# -*- coding: utf-8 -*-

from django.db import models


#Exam Model
class Exam(models.Model):

    class Meta(object):
        verbose_name = 'Іспит'
        verbose_name_plural = 'Іспити'

    exams_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Іспит')

    exams_date = models.DateField(
        blank=False,
        verbose_name='Дата та час проведення іспиту',
        null=True)

    professor = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Прізвище')

    def __str__(self):
        return '{0}'.format(self.exams_name)
