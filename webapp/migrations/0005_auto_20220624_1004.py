# Generated by Django 3.2.12 on 2022-06-24 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_version_abbreviation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verse',
            name='references',
        ),
        migrations.AddField(
            model_name='reference',
            name='book',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='chapters',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='text',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reference',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verse_fk', to='webapp.verse'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='verse',
            field=models.IntegerField(),
        ),
    ]
