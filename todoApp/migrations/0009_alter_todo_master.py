# Generated by Django 3.2 on 2021-12-30 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0008_auto_20211230_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoApp.master'),
        ),
    ]
