from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0044_wbi_hh_type'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_village_livelihood AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.livelihood_1,
                bns_wbi_hh.village,
                bns_wbi_hh.district,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.livelihood_1, bns_wbi_hh.village, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_village_livelihood;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_district_livelihood AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.livelihood_1,
                bns_wbi_hh.district,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.livelihood_1, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_district_livelihood;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_landscape_livelihood AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.livelihood_1,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.livelihood_1, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_landscape_livelihood;")
        ]
