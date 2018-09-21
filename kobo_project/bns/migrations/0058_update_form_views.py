from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0057_bns_form_prices_update_rule'),
    ]
    operations = [
        migrations.RunSQL(
            """
            DROP VIEW bns_form;
    
            CREATE OR REPLACE VIEW bns_form AS
             SELECT kobo_kobodata.dataset_id,
                kobo_kobodata.auth_user_id,
                kobo_kobodata.dataset_name,
                kobo_kobodata.dataset_year,
                kobo_kobodata.dataset_owner,
                kobo_kobodata.dataset_uuid,
                kobo_kobodata.last_submission_time,
                kobo_kobodata.last_update_time,
                kobo_kobodata.last_checked_time,
                kobo_kobodata.kobo_managed
               FROM kobo_kobodata
              WHERE 'bns'::text = ANY (kobo_kobodata.tags);
            """,
            reverse_sql="DROP VIEW bns_form;"),

        migrations.RunSQL(
            """
            DROP VIEW bns_form_price;

            CREATE OR REPLACE VIEW bns_form_price AS
             SELECT a.dataset_id,
                a.auth_user_id,
                a.dataset_name,
                b.dataset_name AS related_dataset,
                b.dataset_uuid AS related_uuid,
                a.dataset_year,
                a.dataset_owner,
                a.dataset_uuid,
                a.last_submission_time,
                a.last_update_time,
                a.last_checked_time,
                a.kobo_managed
               FROM kobo_kobodata a,
                LATERAL unnest(a.tags) t(t)
                 JOIN kobo_kobodata b ON t.t = b.dataset_uuid
              WHERE 'bnsprice'::text = ANY (a.tags);
              
            CREATE OR REPLACE RULE bns_form_price_upd AS
                ON UPDATE TO bns_form_price DO INSTEAD
                  UPDATE kobo_kobodata SET last_update_time = new.last_update_time
                    WHERE kobo_kobodata.dataset_id = old.dataset_id;
            """,
            reverse_sql="DROP VIEW bns_form_price;")
    ]