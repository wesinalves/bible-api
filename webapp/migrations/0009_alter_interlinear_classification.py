# Generated by Django 3.2.12 on 2022-06-30 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20220625_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interlinear',
            name='classification',
            field=models.TextField(),
        ),
    ]
