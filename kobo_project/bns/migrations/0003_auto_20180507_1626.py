# Generated by Django 2.0.5 on 2018-05-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0002_auto_20180507_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answergps',
            name='instace_id',
        ),
        migrations.AddField(
            model_name='answergps',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
