# Generated by Django 2.1.2 on 2018-12-10 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_remotetable_num_rows_last'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remotetable',
            name='num_rows_last',
        ),
    ]