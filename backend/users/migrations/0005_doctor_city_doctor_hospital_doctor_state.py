# Generated by Django 5.1.3 on 2024-11-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_report_patients_report_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='doctor',
            name='state',
            field=models.CharField(default='', max_length=255),
        ),
    ]