from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0034_auto_20180624_1837'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_hh AS 
             WITH w AS (
                     SELECT a.dataset_uuid_id,
                        gs.gs,
                        sum(gs.necessary::integer)::numeric / count(a.dataset_uuid_id)::numeric AS weight
                       FROM bns_answergs gs
                         JOIN bns_answer a ON gs.answer_id = a.answer_id
                      GROUP BY a.dataset_uuid_id, gs.gs
                     HAVING (sum(gs.necessary::integer)::numeric / count(a.dataset_uuid_id)::numeric) > 0.5
                    ), s AS (
                     SELECT a.dataset_uuid_id,
                        k.dataset_year,
                        a.village,
                        a.district,
                        a.landscape,
                        a.hh_id,
                        a.livelihood_1,
                        m.gender,
                        m.ethnicity,
                        a.hh_type_control,
                        a.hh_type_org_benef,
                        a.hh_type_other_benef,
                        gs.gs,
                        gs.have,
                        w_1.weight,
                        gs.have::integer::numeric * w_1.weight AS score
                       FROM bns_answergs gs
                         JOIN bns_answer a ON gs.answer_id = a.answer_id
                         JOIN bns_answerhhmembers m ON gs.answer_id = m.answer_id
                         JOIN w w_1 ON a.dataset_uuid_id = w_1.dataset_uuid_id AND gs.gs = w_1.gs
                         JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
                      WHERE m.head
                    )
             SELECT row_number() OVER () AS id,
                s.dataset_uuid_id,
                s.dataset_year,
                s.hh_id,
                s.village,
                s.district,
                s.landscape,
                s.livelihood_1,
                s.gender,
                s.ethnicity,
                s.hh_type_control,
                s.hh_type_org_benef,
                s.hh_type_other_benef,
                round(sum(s.score), 2) AS hh_score,
                round(sum(w.weight), 2) AS max_score,
                round(sum(s.score) / sum(w.weight), 2) AS wbi
               FROM s
                 JOIN w ON s.dataset_uuid_id = w.dataset_uuid_id AND s.gs = w.gs
              GROUP BY s.dataset_uuid_id, s.hh_id, s.dataset_year, s.village, s.district, s.landscape, s.livelihood_1, s.gender, s.ethnicity, s.hh_type_control, s.hh_type_org_benef, s.hh_type_other_benef
              ORDER BY s.dataset_uuid_id, s.hh_id;
            """,
            reverse_sql="DROP VIEW bns_wbi_hh;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW public.bns_wbi_village AS
             SELECT row_number() OVER() AS id,
               bns_wbi_hh.dataset_uuid_id,
               bns_wbi_hh.dataset_year,
               bns_wbi_hh.village,
               bns_wbi_hh.district,
               bns_wbi_hh.landscape,
               round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
               round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
               count(bns_wbi_hh.hh_id) AS n
             FROM bns_wbi_hh
             GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.village, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_village;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW public.bns_wbi_district AS
             SELECT row_number() OVER() AS id,
               bns_wbi_hh.dataset_uuid_id,
               bns_wbi_hh.dataset_year,
               bns_wbi_hh.district,
               bns_wbi_hh.landscape,
               round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
               round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
               count(bns_wbi_hh.hh_id) AS n
             FROM bns_wbi_hh
             GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW public.bns_wbi_landscape AS
             SELECT row_number() OVER() AS id,
               bns_wbi_hh.dataset_uuid_id,
               bns_wbi_hh.dataset_year,
               bns_wbi_hh.landscape,
               round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
               round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
               count(bns_wbi_hh.hh_id) AS n
             FROM bns_wbi_hh
             GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_landscape;")
        ]
