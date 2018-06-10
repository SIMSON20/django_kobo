from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0024_auto_20180610_2210'),
    ]
    operations = [
        migrations.RunSQL(
            """ 
            CREATE OR REPLACE VIEW bns_ethnicity_per_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                a.district,
                a.village,
                k.dataset_year,
                m.ethnicity,
                round(count(m.ethnicity)::numeric / sum(count(m.ethnicity)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, a.district, a.village, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.ethnicity IS NOT NULL
              GROUP BY a.dataset_uuid_id, a.landscape, a.district, a.village, m.ethnicity, k.dataset_year
              ORDER BY a.dataset_uuid_id, a.landscape, a.district, a.village, k.dataset_year;
            """, reverse_sql="DROP VIEW bns_ethnicity_per_village;"),

        migrations.RunSQL(
            """ 
            CREATE OR REPLACE VIEW bns_ethnicity_per_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                a.district,
                k.dataset_year,
                m.ethnicity,
                round(count(m.ethnicity)::numeric / sum(count(m.ethnicity)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, a.district, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.ethnicity IS NOT NULL
              GROUP BY a.dataset_uuid_id, a.landscape, a.district, m.ethnicity, k.dataset_year
              ORDER BY a.dataset_uuid_id, a.landscape, a.district, k.dataset_year;
            """, reverse_sql="DROP VIEW bns_ethnicity_per_district;"),

        migrations.RunSQL(
            """ 
            CREATE OR REPLACE VIEW bns_ethnicity_per_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                k.dataset_year,
                m.ethnicity,
                round(count(m.ethnicity)::numeric / sum(count(m.ethnicity)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.ethnicity IS NOT NULL
              GROUP BY a.dataset_uuid_id, a.landscape, m.ethnicity, k.dataset_year
              ORDER BY a.dataset_uuid_id, a.landscape, k.dataset_year;
            """, reverse_sql="DROP VIEW bns_ethnicity_per_landscape;")

    ]

