# Generated by Django 2.1 on 2018-08-28 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasksapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containertaskinstance',
            name='name',
            field=models.CharField(blank=True, help_text='An optional non-unique name for the task instance', max_length=200),
        ),
        migrations.AlterField(
            model_name='containertasktype',
            name='name',
            field=models.CharField(help_text='The name of the task', max_length=200),
        ),
        migrations.AlterField(
            model_name='executabletaskinstance',
            name='name',
            field=models.CharField(blank=True, help_text='An optional non-unique name for the task instance', max_length=200),
        ),
        migrations.AlterField(
            model_name='executabletasktype',
            name='name',
            field=models.CharField(help_text='The name of the task', max_length=200),
        ),
    ]
