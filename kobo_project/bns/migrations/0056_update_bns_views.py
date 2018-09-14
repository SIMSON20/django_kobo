from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0055_update_bns_views'),
    ]
    operations = [

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
                a.last_checked_time
               FROM kobo_kobodata a,
                LATERAL unnest(a.tags) t(t)
                 JOIN kobo_kobodata b ON t.t = b.dataset_uuid
              WHERE 'bnsprice'::text = ANY (a.tags);
            """,
            reverse_sql="DROP VIEW bns_form_price;")
        ]