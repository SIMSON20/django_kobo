from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns',
         '0048_wealthidxperdistrict_wealthidxperhh_wealthidxperlandscape_wealthidxpervillage'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_hh_diff_2015_2017 AS 
             WITH wbi_2015 AS (
                     SELECT upper(bns_wbi_hh.hh_id) AS hh_id,
                        bns_wbi_hh.wbi
                       FROM bns_wbi_hh
                      WHERE bns_wbi_hh.dataset_year::double precision = 2015::double precision
                    ), wbi_2017 AS (
                     SELECT b.dataset_uuid_id,
                        a.answer_id,
                        upper(b.hh_id) AS hh_id,
                        b.wbi,
                        b.hh_type_control,
                        b.hh_type_org_benef,
                        b.hh_type_other_benef,
                        b.village,
                        b.district,
                        b.landscape,
                        g.geom
                       FROM bns_wbi_hh b
                         JOIN bns_answer a ON a.hh_id = b.hh_id AND a.dataset_uuid_id = b.dataset_uuid_id
                         LEFT JOIN bns_answergps g ON a.answer_id = g.answer_id
                      WHERE b.dataset_year::double precision = 2017::double precision
                    )
             SELECT row_number() OVER () AS gid,
                wbi_2017.dataset_uuid_id,
                wbi_2015.hh_id,
                wbi_2017.village,
                wbi_2017.district,
                wbi_2017.landscape,
                wbi_2017.hh_type_control,
                wbi_2017.hh_type_org_benef,
                wbi_2017.hh_type_other_benef,
                wbi_2015.wbi AS wbi_2015,
                wbi_2017.wbi AS wbi_2017,
                wbi_2017.wbi - wbi_2015.wbi AS wbi_diff,
                wbi_2017.geom
               FROM wbi_2015
                 JOIN wbi_2017 ON wbi_2015.hh_id = wbi_2017.hh_id;
            """,
            reverse_sql="DROP VIEW bns_wbi_hh_diff_2015_2017;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_village_diff_2015_2017 AS 
             SELECT row_number() OVER () AS gid,
                bns_wbi_hh_diff_2015_2017.dataset_uuid_id,
                bns_wbi_hh_diff_2015_2017.village,
                bns_wbi_hh_diff_2015_2017.district,
                bns_wbi_hh_diff_2015_2017.landscape,
                bns_wbi_hh_diff_2015_2017.hh_type_control,
                avg(bns_wbi_hh_diff_2015_2017.wbi_2015) AS avg_wbi_2015,
                avg(bns_wbi_hh_diff_2015_2017.wbi_2017) AS avg_wbi_2017,
                avg(bns_wbi_hh_diff_2015_2017.wbi_diff) AS avg_wbi_diff,
                st_centroid(st_collect(bns_wbi_hh_diff_2015_2017.geom)) AS geom
               FROM bns_wbi_hh_diff_2015_2017
              GROUP BY bns_wbi_hh_diff_2015_2017.dataset_uuid_id, bns_wbi_hh_diff_2015_2017.village, bns_wbi_hh_diff_2015_2017.district, bns_wbi_hh_diff_2015_2017.landscape, bns_wbi_hh_diff_2015_2017.hh_type_control
              ORDER BY bns_wbi_hh_diff_2015_2017.dataset_uuid_id, bns_wbi_hh_diff_2015_2017.landscape, bns_wbi_hh_diff_2015_2017.district, bns_wbi_hh_diff_2015_2017.village, bns_wbi_hh_diff_2015_2017.hh_type_control;
            """,
            reverse_sql="DROP VIEW bns_wbi_village_diff_2015_2017;")
    ]