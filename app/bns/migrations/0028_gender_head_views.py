from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0027_auto_20180610_2303'),
    ]
    operations = [
        migrations.RunSQL("DROP VIEW bns_gender_head_per_village;"),
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_gender_head_per_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                a.district,
                a.village,
                k.dataset_year,
                m.gender,
                round(count(m.head)::numeric / sum(count(m.head)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, a.district, a.village, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.head
              GROUP BY a.dataset_uuid_id, a.landscape, a.district, a.village, k.dataset_year, m.gender
              ORDER BY a.dataset_uuid_id, a.landscape, a.district, a.village, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_gender_head_per_village;"),

        migrations.RunSQL("DROP VIEW bns_gender_head_per_district;"),
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_gender_head_per_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                a.district,
                k.dataset_year,
                m.gender,
                round(count(m.head)::numeric / sum(count(m.head)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, a.district, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.head
              GROUP BY a.dataset_uuid_id, a.landscape, a.district, k.dataset_year, m.gender
              ORDER BY a.dataset_uuid_id, a.landscape, a.district, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_gender_head_per_district;"),

        migrations.RunSQL("DROP VIEW bns_gender_head_per_landscape;"),
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_gender_head_per_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                k.dataset_year,
                m.gender,
                round(count(m.head)::numeric / sum(count(m.head)) OVER (PARTITION BY a.dataset_uuid_id, a.landscape, k.dataset_year) * 100::numeric, 2) AS ratio,
                count(a.hh_id) AS n
               FROM bns_answerhhmembers m
                 JOIN bns_answer a ON m.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              WHERE m.head
              GROUP BY a.dataset_uuid_id, a.landscape, k.dataset_year, m.gender
              ORDER BY a.dataset_uuid_id, a.landscape, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_gender_head_per_landscape;")
    ]
