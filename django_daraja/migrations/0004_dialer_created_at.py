# Generated by Django 4.1.3 on 2023-04-14 16:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_daraja', '0003_remove_dialer_id_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
