# Generated by Django 3.2.3 on 2021-06-20 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_criterion_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['-id']},
        ),
    ]
