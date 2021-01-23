# Generated by Django 2.2.17 on 2021-01-23 15:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='tel',
            field=models.CharField(default=django.utils.timezone.now, max_length=15, verbose_name='電話番号'),
            preserve_default=False,
        ),
    ]
