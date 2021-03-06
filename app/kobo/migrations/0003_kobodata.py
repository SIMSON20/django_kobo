# Generated by Django 2.0.5 on 2018-05-09 21:15

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kobo', '0002_auto_20180502_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='KoboData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_id', models.BigIntegerField()),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('dataset', django.contrib.postgres.fields.jsonb.JSONField()),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kobo.Connection')),
            ],
        ),
    ]
