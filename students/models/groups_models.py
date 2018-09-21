from django.db import models


# Group Model
class Group(models.Model):

    class Meta(object):
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Назва')

    leader = models.OneToOneField(
        'Student',
        verbose_name='Староста',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name='Додаткові нотатки')

    def __str__(self):
        return self.title
