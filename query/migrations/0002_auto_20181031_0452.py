# Generated by Django 2.1.2 on 2018-10-31 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='num_columns',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='query',
            name='num_rows',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
