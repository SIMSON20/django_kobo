from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('kobo', '0014_auto_20180921_1443'),
        ('nrgt', '0002_auto_20181107_2142'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW nrgt_form AS
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
              WHERE 'nrgt'::text = ANY (kobo_kobodata.tags);
            """,
            reverse_sql="DROP VIEW nrgt_form;"),
        ]