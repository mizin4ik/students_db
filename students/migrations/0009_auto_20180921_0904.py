# Generated by Django 2.1 on 2018-09-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20180917_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='exam',
        ),
        migrations.AddField(
            model_name='exam',
            name='exams_group',
            field=models.ManyToManyField(blank=True, to='students.Group'),
        ),
    ]