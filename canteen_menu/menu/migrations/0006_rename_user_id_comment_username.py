# Generated by Django 4.2.2 on 2023-09-11 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='username',
        ),
    ]
