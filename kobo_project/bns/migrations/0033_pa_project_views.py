from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0032_auto_20180624_1813'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_project_pa_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                k.dataset_year,
                a.village,
                a.district,
                a.landscape,
                round(sum(a.benef_project::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_project,
                round(sum(a.know_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_know_pa,
                round(sum(a.benef_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_pa,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.village, a.district, a.landscape
              ORDER BY a.dataset_uuid_id, k.dataset_year, a.village, a.district, a.landscape;
            """,
            reverse_sql="DROP VIEW bns_project_pa_village;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_project_pa_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                k.dataset_year,
                a.district,
                a.landscape,
                round(sum(a.benef_project::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_project,
                round(sum(a.know_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_know_pa,
                round(sum(a.benef_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_pa,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.district, a.landscape
              ORDER BY a.dataset_uuid_id, k.dataset_year, a.district, a.landscape;
            """,
            reverse_sql="DROP VIEW bns_project_pa_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_project_pa_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                k.dataset_year,
                a.landscape,
                round(sum(a.benef_project::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_project,
                round(sum(a.know_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_know_pa,
                round(sum(a.benef_pa::integer)::numeric / count(a.hh_id)::numeric, 2) AS perc_benef_pa,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.landscape
              ORDER BY a.dataset_uuid_id, k.dataset_year, a.landscape;
            """,
            reverse_sql="DROP VIEW bns_project_pa_landscape;"),
    ]