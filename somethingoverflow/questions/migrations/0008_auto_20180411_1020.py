# Generated by Django 2.0.4 on 2018-04-11 10:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0007_question_tags'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('post', 'author', 'question', 'status')},
        ),
    ]