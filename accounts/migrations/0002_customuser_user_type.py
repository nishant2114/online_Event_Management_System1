# Generated by Django 5.1.3 on 2024-11-26 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('hall_provider', 'Hall Provider')], default='user', max_length=20),
        ),
    ]