# Generated by Django 2.1.2 on 2018-12-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotetable',
            name='owner',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='remotetable',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
