from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bns', '0036_auto_20180912_1603'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE INDEX bns_answer_answer_id_idx
              ON public.bns_answer
              USING btree
              (answer_id);
            """,
            reverse_sql="DROP INDEX bns_answer_answer_id_idx;"),

        migrations.RunSQL(
            """
            CREATE INDEX bns_answergps_answer_id_idx
              ON public.bns_answergps
              USING btree
              (answer_id);
              """,
            reverse_sql="DROP INDEX bns_answergps_answer_id_idx;"),

        migrations.RunSQL(
            """
                    
            CREATE INDEX bns_answergps_geom_idx
              ON public.bns_answergps
              USING gist
              (geom);
            """,
            reverse_sql="DROP INDEX bns_answergps_geom_idx;"),

        migrations.RunSQL(
            """
            CREATE INDEX bns_answergs_gs_idx
              ON public.bns_answergs
              USING btree
              (gs);
            """,
            reverse_sql="DROP INDEX bns_answergs_gs_idx;")
    ]
