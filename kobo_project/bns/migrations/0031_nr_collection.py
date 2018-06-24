from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0030_auto_20180610_2329'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_nr_collect_village AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                nr.nr,
                k.dataset_year,
                a.village,
                a.district,
                a.landscape,
                round(avg(nr.nr_collect), 2) AS avg_collect_week,
                round(sum((nr.nr_collect > 0)::integer)::numeric / count(nr.nr)::numeric * 100::numeric, 2) AS perc_hh_collect,
                round(stddev_samp(nr.nr_collect), 2) AS stddev_collect_week,
                count(a.hh_id) AS n
               FROM bns_answernr nr
                 JOIN bns_answer a ON nr.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.village, a.district, a.landscape, nr.nr
              ORDER BY a.dataset_uuid_id, nr.nr, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_nr_collect_village;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_nr_collect_district AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                nr.nr,
                k.dataset_year,
                a.district,
                a.landscape,
                round(avg(nr.nr_collect), 2) AS avg_collect_week,
                round(sum((nr.nr_collect > 0)::integer)::numeric / count(nr.nr)::numeric * 100::numeric, 2) AS perc_hh_collect,
                round(stddev_samp(nr.nr_collect), 2) AS stddev_collect_week,
                count(a.hh_id) AS n
               FROM bns_answernr nr
                 JOIN bns_answer a ON nr.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.district, a.landscape, nr.nr
              ORDER BY a.dataset_uuid_id, nr.nr, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_nr_collect_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_nr_collect_landscape AS 
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                nr.nr,
                k.dataset_year,
                a.landscape,
                round(avg(nr.nr_collect), 2) AS avg_collect_week,
                round(sum((nr.nr_collect > 0)::integer)::numeric / count(nr.nr)::numeric * 100::numeric, 2) AS perc_hh_collect,
                round(stddev_samp(nr.nr_collect), 2) AS stddev_collect_week,
                count(a.hh_id) AS n
               FROM bns_answernr nr
                 JOIN bns_answer a ON nr.answer_id = a.answer_id
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.landscape, nr.nr
              ORDER BY a.dataset_uuid_id, nr.nr, k.dataset_year;
            """,
            reverse_sql="DROP VIEW bns_nr_collect_landscape;"),

    ]