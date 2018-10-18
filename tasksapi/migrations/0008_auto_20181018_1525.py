# Generated by Django 2.1.2 on 2018-10-18 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasksapi', '0007_executabletasktype_json_file_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executabletasktype',
            name='json_file_option',
            field=models.CharField(blank=True, default=None, help_text="The name of a command line option, e.g., --json-file, which accepts a JSON-encoded file for the task to run. If this value is non-null, then the instance's JSON arguments are written to a file and this file is passed to the command (cf. normal behaviour where the JSON arguments are passed as a single argument to the task).", max_length=50, null=True, verbose_name='JSON file option'),
        ),
    ]
