from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0043_wbi_gender'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_village_hh_type AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.hh_type_control,
                bns_wbi_hh.hh_type_org_benef,
                bns_wbi_hh.hh_type_other_benef,
                bns_wbi_hh.village,
                bns_wbi_hh.district,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.village, bns_wbi_hh.hh_type_control, bns_wbi_hh.hh_type_org_benef, bns_wbi_hh.hh_type_other_benef, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_village_hh_type;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_district_hh_type AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.hh_type_control,
                bns_wbi_hh.hh_type_org_benef,
                bns_wbi_hh.hh_type_other_benef,
                bns_wbi_hh.district,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.hh_type_control, bns_wbi_hh.hh_type_org_benef, bns_wbi_hh.hh_type_other_benef, bns_wbi_hh.district, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_district_hh_type;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wbi_landscape_hh_type AS 
             SELECT row_number() OVER () AS id,
                bns_wbi_hh.dataset_uuid_id,
                bns_wbi_hh.dataset_year,
                bns_wbi_hh.hh_type_control,
                bns_wbi_hh.hh_type_org_benef,
                bns_wbi_hh.hh_type_other_benef,
                bns_wbi_hh.landscape,
                round(avg(bns_wbi_hh.wbi), 2) AS avg_wbi,
                round(stddev_samp(bns_wbi_hh.wbi), 2) AS stddev_wbi,
                count(bns_wbi_hh.hh_id) AS n
               FROM bns_wbi_hh
              GROUP BY bns_wbi_hh.dataset_uuid_id, bns_wbi_hh.dataset_year, bns_wbi_hh.hh_type_control, bns_wbi_hh.hh_type_org_benef, bns_wbi_hh.hh_type_other_benef, bns_wbi_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wbi_landscape_hh_type;")
        ]
