# Generated by Django 3.2.12 on 2022-06-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20220603_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='abbreviation',
            field=models.CharField(max_length=20),
        ),
    ]