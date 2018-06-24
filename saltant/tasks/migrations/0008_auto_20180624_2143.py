# Generated by Django 2.0.6 on 2018-06-24 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20180624_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskqueue',
            name='description',
            field=models.TextField(blank=True, default='', help_text='A description of the queue'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='description',
            field=models.TextField(blank=True, default='', help_text='A description of the task'),
            preserve_default=False,
        ),
    ]
