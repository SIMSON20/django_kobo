from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0052_auto_20180914_1417'),
    ]
    operations = [
        migrations.RunSQL(
            """
            DROP VIEW bns_form;
            
            CREATE OR REPLACE VIEW bns_form AS
             SELECT row_number() OVER () AS id,
                kobo_kobodata.dataset_name,
                kobo_kobodata.dataset_year,
                kobo_kobodata.dataset_owner,
                kobo_kobodata.dataset_uuid,
                kobo_kobodata.last_submission_time,
                kobo_kobodata.last_update_time,
                kobo_kobodata.last_checked_time
               FROM kobo_kobodata
              WHERE 'bns'::text = ANY (kobo_kobodata.tags);
            """,
            reverse_sql="DROP VIEW bns_form;"),

        migrations.RunSQL(
            """
            DROP VIEW bns_form_price;
            
            CREATE OR REPLACE VIEW bns_form_price AS
             SELECT row_number() OVER () AS id,
                a.dataset_name,
                b.dataset_name AS related_dataset,
                a.dataset_year,
                a.dataset_owner,
                a.dataset_uuid,
                a.last_submission_time,
                a.last_update_time,
                a.last_checked_time
               FROM kobo_kobodata a,
                LATERAL unnest(a.tags) t(t)
                 JOIN kobo_kobodata b ON t.t = b.dataset_uuid
              WHERE 'bnsprice'::text = ANY (a.tags);
            """,
            reverse_sql="DROP VIEW bns_form_price;")
        ]