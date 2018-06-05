from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0021_ame_views'),
    ]

    operations = [
        migrations.RunSQL(
            """   
                DROP VIEW bns_ame_per_hh CASCADE;
            """),

        migrations.RunSQL(
            """   
            CREATE OR REPLACE VIEW bns_ame_per_hh AS
             SELECT row_number() OVER () AS id,
                k.dataset_uuid as dataset_uuid_id,
                d.hh_id,
                k.dataset_year,
                d.village,
                d.district,
                d.landscape,
                 round(sum(a.ame)::numeric, 2) AS hh_ame
               FROM bns_answerhhmembers m
                 JOIN bns_answer d ON m.answer_id = d.answer_id
                 JOIN kobo_kobodata k ON d.dataset_uuid_id = k.dataset_uuid
                 JOIN bns_ame a ON a.age::double precision = (k.dataset_year::double precision - m.birth::double precision) AND a.gender = m.gender
              GROUP BY k.dataset_uuid,  d.hh_id, k.dataset_year, d.village, d.district, d.landscape;
            """, reverse_sql="DROP VIEW bns_ame_per_hh;"),

        migrations.RunSQL(
            """   
            CREATE OR REPLACE VIEW bns_ame_per_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.dataset_year,
                a.village,
                a.district,
                a.landscape,
                round(avg(a.hh_ame)::numeric, 2) AS avg_hh_ame,
                round(stddev_samp(a.hh_ame)::numeric, 2) AS stddev_hh_ame,
                count(a.hh_id) AS n
               FROM bns_ame_per_hh a
              GROUP BY a.dataset_uuid_id, a.dataset_year, a.village, a.district, a.landscape;
            """, reverse_sql="DROP VIEW bns_ame_per_village;"),

        migrations.RunSQL(
            """   
            CREATE OR REPLACE VIEW bns_ame_per_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.dataset_year,
                a.district,
                a.landscape,
                round(avg(a.hh_ame)::numeric, 2) AS avg_hh_ame,
                round(stddev_samp(a.hh_ame)::numeric, 2) AS stddev_hh_ame,
                count(a.hh_id) AS n
               FROM bns_ame_per_hh a
              GROUP BY a.dataset_uuid_id, a.dataset_year, a.district, a.landscape;
            """, reverse_sql="DROP VIEW bns_ame_per_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_ame_per_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.dataset_year,
                a.landscape,
                round(avg(a.hh_ame)::numeric, 2) AS avg_hh_ame,
                round(stddev_samp(a.hh_ame)::numeric, 2) AS stddev_hh_ame,
                count(a.hh_id) AS n
               FROM bns_ame_per_hh a
              GROUP BY a.dataset_uuid_id, a.dataset_year, a.landscape;
            """, reverse_sql="DROP VIEW bns_ame_per_landscape;")
        ]

