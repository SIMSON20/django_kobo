# Generated by Django 2.0.5 on 2018-09-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0045_wbi_livelihood'),
    ]

    operations = [
        migrations.CreateModel(
            name='WBIPerDistrictEthnicity',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('ethnicity', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_district_ethnicity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerDistrictGender',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_district_gender',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerDistrictHHType',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('hh_type', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_district_hh_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerDistrictLivelihood',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('livelihood_1', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_district_livelihood',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerLandscapeEthnicity',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('ethnicity', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_landscape_ethnicity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerLandscapeGender',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_landscape_gender',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerLandscapeHHType',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('hh_type', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_landscape_hh_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerLandscapeLivelihood',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('livelihood_1', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_landscape_livelihood',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerVillageEthnicity',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('ethnicity', models.TextField(blank=True, null=True)),
                ('village', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_village_ethnicity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerVillageGender',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('village', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_village_gender',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerVillageHHType',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('hh_type', models.TextField(blank=True, null=True)),
                ('village', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_village_hh_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WBIPerVillageLivelihood',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dataset_year', models.IntegerField(blank=True, null=True)),
                ('livelihood_1', models.TextField(blank=True, null=True)),
                ('village', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('landscape', models.TextField(blank=True, null=True)),
                ('avg_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('stddev_wbi', models.DecimalField(blank=True, decimal_places=6, max_digits=29, null=True)),
                ('n', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bns_wbi_village_livelihood',
                'managed': False,
            },
        ),
    ]