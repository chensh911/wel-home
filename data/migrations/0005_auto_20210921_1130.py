# Generated by Django 3.2.5 on 2021-09-21 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_home'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='door',
            field=models.SmallIntegerField(default=1, verbose_name='门'),
        ),
        migrations.AddField(
            model_name='home',
            name='window',
            field=models.SmallIntegerField(default=1, verbose_name='窗'),
        ),
    ]