# Generated by Django 4.2.2 on 2023-07-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_jobdescription_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdescription',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
