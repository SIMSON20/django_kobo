from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0028_gender_head_views'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_livelihood_nb_per_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.village,
                a.district,
                a.landscape,
                k.dataset_year,
                round(avg(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS avg_lh_number,
                round(stddev_samp(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS stddev_lh_number,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, a.village, a.district, a.landscape, k.dataset_year
              ORDER BY a.landscape, a.district, a.village, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_livelihood_nb_per_village;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_livelihood_nb_per_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.district,
                a.landscape,
                k.dataset_year,
                round(avg(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS avg_lh_number,
                round(stddev_samp(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS stddev_lh_number,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, a.district, a.landscape, k.dataset_year
              ORDER BY a.landscape, a.district, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_livelihood_nb_per_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_livelihood_nb_per_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                a.landscape,
                k.dataset_year,
                round(avg(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS avg_lh_number,
                round(stddev_samp(
                    CASE
                        WHEN length(a.livelihood_1)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_2)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_3)::boolean THEN 1
                        ELSE 0
                    END +
                    CASE
                        WHEN length(a.livelihood_4)::boolean THEN 1
                        ELSE 0
                    END), 2) AS stddev_lh_number,
                count(a.hh_id) AS n
               FROM bns_answer a
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, a.landscape, k.dataset_year
              ORDER BY a.landscape, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_livelihood_nb_per_landscape;")
    ]
