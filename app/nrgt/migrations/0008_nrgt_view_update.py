from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nrgt', '0007_nrgtanswergs_last_update'),
    ]
    operations = [
        migrations.RunSQL(
            """
            DROP VIEW nrgt_group_scores CASCADE;

            CREATE OR REPLACE VIEW nrgt_group_scores AS
            SELECT
                k.dataset_uuid as dataset_uuid_id,
                a.landscape,
                a.gov_group,
                k.dataset_year,
                round(avg(gs.legitimacy), 2) AS legitimacy,
                round(avg(gs.accountability), 2) AS accountability,
                round(avg(gs.transparency), 2) AS transparency,
                round(avg(gs.participation), 2) AS participation,
                round(avg(gs.instutional_framework), 2) AS instutional_framework,
                round(avg(gs.fairness), 2) AS fairness,
                round(avg(gs.motivation), 2) AS motivation,
                round(avg(gs.knowledge_skills), 2) AS knowledge_skills,
                round(avg(gs.resources), 2) AS resources,
                round(avg(gs.held_accountable), 2) AS held_accountable,
                round(avg(gs.enact_decision), 2) AS enact_decision,
                round(avg(gs.diversity), 2) AS diversity
            FROM 
                nrgt_nrgtanswergs gs
                JOIN nrgt_nrgtanswer a ON gs.answer_id = a.answer_id 
                JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
            GROUP BY 
                k.dataset_uuid, a.landscape, a.gov_group, k.dataset_year;
            """,
            reverse_sql="DROP VIEW nrgt_group_scores;"),

        migrations.RunSQL(
            """
                CREATE OR REPLACE VIEW nrgt_group_attributes AS 
                SELECT
                    gs.dataset_uuid_id,
                    gs.landscape,
                    gs.gov_group,
                    gs.dataset_year,
                    round((gs.legitimacy + gs.accountability + gs.transparency + 
                            gs.participation + gs.fairness) / 5::numeric, 2) AS autority,
                    round((gs.knowledge_skills + gs.resources + 
                            gs.instutional_framework + gs.motivation) / 4::numeric, 2) AS capacity,
                    round((gs.held_accountable + gs.enact_decision) / 2::numeric, 2) AS power,
                    gs.diversity
                FROM
                    nrgt_group_scores gs;
                """,
            reverse_sql="DROP VIEW nrgt_group_attributes;"),
    ]
