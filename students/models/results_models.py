# -*- coding: utf-8 -*-

from django.db import models


#Result Model
class Result(models.Model):

    class Meta(object):
        verbose_name = 'Результати іспиту'
        verbose_name_plural = 'Результати іспитів'

    student = models.ForeignKey(
        'Student',
        verbose_name='Студент',
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    exam = models.ForeignKey(
        'Exam',
        verbose_name='Іспит',
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    result = models.IntegerField(
        verbose_name='Результати іспиту',
        null=True)

    def __str__(self):
        return self.exam.exams_name

