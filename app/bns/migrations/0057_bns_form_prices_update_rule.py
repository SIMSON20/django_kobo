from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0056_update_bns_views'),
    ]
    operations = [

        migrations.RunSQL(
            """
            CREATE OR REPLACE RULE bns_form_price_upd AS
                ON UPDATE TO bns_form_price DO INSTEAD
                  UPDATE kobo_kobodata SET last_update_time = new.last_update_time
                    WHERE kobo_kobodata.dataset_id = old.dataset_id;
             """,
            reverse_sql="DROP RULE bns_form_price_upd ON bns_form_price;")
        ]