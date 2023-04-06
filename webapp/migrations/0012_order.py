# Generated by Django 4.0.2 on 2023-04-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_alter_verse_dictionaries_alter_verse_intelinears'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(blank=True, default='', max_length=1000)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('checkout_url', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
    ]
