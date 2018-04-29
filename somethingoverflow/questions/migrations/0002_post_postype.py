# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-09 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postype',
            field=models.CharField(choices=[('q', 'Question'), ('a', 'Answer')], default='q', max_length=1),
        ),
    ]