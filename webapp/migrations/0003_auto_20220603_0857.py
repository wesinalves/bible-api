# Generated by Django 3.2.12 on 2022-06-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20220601_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idiom',
            name='abbreviation',
        ),
        migrations.AddField(
            model_name='idiom',
            name='native_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
