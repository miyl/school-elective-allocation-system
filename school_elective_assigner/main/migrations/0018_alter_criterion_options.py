# Generated by Django 3.2.3 on 2021-06-20 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210619_2331'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criterion',
            options={'ordering': ['type', '-all'], 'verbose_name_plural': 'criteria'},
        ),
    ]
