# Generated by Django 3.2.3 on 2021-05-27 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210525_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='description_en',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='name_en',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description_da',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name_da',
        ),
    ]
