# Generated by Django 3.2.9 on 2021-11-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='user',
        ),
    ]
