# Generated by Django 2.0.6 on 2018-07-18 21:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasksapi', '0002_auto_20180716_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskqueue',
            name='private',
            field=models.BooleanField(default=False, help_text='A boolean specifying whether other users besides the queue creator can use the queue.'),
        ),
        migrations.AddField(
            model_name='taskqueue',
            name='user',
            field=models.ForeignKey(default=1, help_text='The creater of the queue', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
