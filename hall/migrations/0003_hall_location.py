# Generated by Django 5.1.3 on 2024-11-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='location',
            field=models.CharField(default='vizag', max_length=100),
        ),
    ]