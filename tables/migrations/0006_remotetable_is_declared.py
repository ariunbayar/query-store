# Generated by Django 2.1.2 on 2018-12-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0005_remove_remotetable_num_rows_last'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotetable',
            name='is_declared',
            field=models.BooleanField(default=False),
        ),
    ]
