# Generated by Django 2.2.17 on 2021-01-23 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='tel',
            field=models.CharField(max_length=15, null=True, verbose_name='電話番号'),
        ),
    ]
