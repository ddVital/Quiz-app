# Generated by Django 4.0.4 on 2022-06-03 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(choices=[('default0', 'default0'), ('default1', 'default1'), ('default2', 'default2'), ('default3', 'default3'), ('default4', 'default4'), ('default5', 'default5')], default='default3', max_length=10),
        ),
    ]
