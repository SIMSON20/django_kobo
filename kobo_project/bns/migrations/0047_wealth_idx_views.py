from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bns', '0046_wbiperdistrictethnicity_wbiperdistrictgender_wbiperdistricthhtype_wbiperdistrictlivelihood_wbiperlan'),
    ]
    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wealth_idx_hh AS 
             WITH p AS (
                     SELECT bns_price.dataset_uuid_id,
                        bns_price.gs,
                        round(avg(bns_price.price)) AS price
                       FROM bns_price
                      GROUP BY bns_price.dataset_uuid_id, bns_price.gs
                    )
             SELECT row_number() OVER () AS id,
                a.dataset_uuid_id,
                k.dataset_year,
                a.hh_id,
                a.village,
                a.district,
                a.landscape,
                sum(gs.quantity::numeric * p.price) AS wealth_idx
               FROM bns_answergs gs
                 JOIN bns_answer a ON gs.answer_id = a.answer_id
                 JOIN p ON a.dataset_uuid_id = p.dataset_uuid_id AND gs.gs = p.gs
                 JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid
              GROUP BY a.dataset_uuid_id, k.dataset_year, a.hh_id, a.village, a.district, a.landscape;
            """,
            reverse_sql="DROP VIEW bns_wealth_idx_hh;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wealth_idx_village AS
             SELECT row_number() OVER() AS id,
                bns_wealth_idx_hh.dataset_uuid_id, 
                bns_wealth_idx_hh.dataset_year,
                bns_wealth_idx_hh.village,
                bns_wealth_idx_hh.district,
                bns_wealth_idx_hh.landscape,
                round(avg(bns_wealth_idx_hh.wealth_idx), 2) AS avg_wealth_idx,
                round(stddev_samp(bns_wealth_idx_hh.wealth_idx), 2) AS stddev_wealth_idx,
                count(bns_wealth_idx_hh.wealth_idx) AS n
             FROM bns_wealth_idx_hh
             GROUP BY bns_wealth_idx_hh.dataset_uuid_id, bns_wealth_idx_hh.dataset_year, bns_wealth_idx_hh.village, bns_wealth_idx_hh.district, bns_wealth_idx_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wealth_idx_village;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wealth_idx_district AS
             SELECT row_number() OVER() AS id,
                bns_wealth_idx_hh.dataset_uuid_id,
                bns_wealth_idx_hh.dataset_year,
                bns_wealth_idx_hh.district,
                bns_wealth_idx_hh.landscape,
                round(avg(bns_wealth_idx_hh.wealth_idx), 2) AS avg_wealth_idx,
                round(stddev_samp(bns_wealth_idx_hh.wealth_idx), 2) AS stddev_wealth_idx,
                count(bns_wealth_idx_hh.wealth_idx) AS n
             FROM bns_wealth_idx_hh
             GROUP BY bns_wealth_idx_hh.dataset_uuid_id, bns_wealth_idx_hh.dataset_year, bns_wealth_idx_hh.district, bns_wealth_idx_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wealth_idx_district;"),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW bns_wealth_idx_landscape AS
             SELECT row_number() OVER() AS id,
                bns_wealth_idx_hh.dataset_uuid_id,
                bns_wealth_idx_hh.dataset_year,
                bns_wealth_idx_hh.landscape,
                round(avg(bns_wealth_idx_hh.wealth_idx), 2) AS avg_wealth_idx,
                round(stddev_samp(bns_wealth_idx_hh.wealth_idx), 2) AS stddev_wealth_idx,
                count(bns_wealth_idx_hh.wealth_idx) AS n
             FROM bns_wealth_idx_hh
             GROUP BY bns_wealth_idx_hh.dataset_uuid_id, bns_wealth_idx_hh.dataset_year, bns_wealth_idx_hh.landscape;
            """,
            reverse_sql="DROP VIEW bns_wealth_idx_landscape;"),

       ]
