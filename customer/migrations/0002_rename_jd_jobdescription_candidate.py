# Generated by Django 4.2.2 on 2023-07-17 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobdescription',
            old_name='jd',
            new_name='candidate',
        ),
    ]
