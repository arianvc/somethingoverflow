# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-09 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20180409_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reactions_for_question', to='questions.Question'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reactions_for_post', to='questions.Post'),
        ),
    ]