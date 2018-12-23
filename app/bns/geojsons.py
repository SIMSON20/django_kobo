from .models import Answer, Landscape


def landscape_boundary(landscape_name):
    """
    Return landscape boundary as GeoJSON
    :param landscape_name:
    :return:
    """
    landscape_boundaries = Landscape.objects.raw("""SELECT 
                                                        id, 
                                                        landscape,  
                                                        ST_AsGeoJSON(geom) as geojson 
                                                    FROM bns_landscape 
                                                    WHERE landscape = '{}' LIMIT 1""".format(landscape_name))

    landscape_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(landscape_boundaries):
        landscape_geojson += '{"type": "Feature", "properties": {"landscape": "%s"}, "geometry": %s }' % \
                             (landscape_name, landscape_boundaries[0].geojson)
    landscape_geojson += ']}'

    return landscape_geojson


def landscape_villages(landscape_name):
    """
    Return landscape villages as GeoJSON
    :param landscape_name:
    :return:
    """
    landscape_villages = Answer.objects.raw("""SELECT row_number() OVER () as answer_id,
                                                dataset_name, 
                                                village, 
                                                ST_AsGeoJSON(ST_SetSRID(ST_MakePoint(avg(long), avg(lat)),4326)) as geojson 
                                            FROM bns_answer a 
                                                JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid 
                                                JOIN bns_answergps g ON a.answer_id = g.answer_id
                                            WHERE landscape = '{}' AND lat != 0 AND long != 0
                                            GROUP BY dataset_name, village""".format(landscape_name))

    village_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(landscape_villages):

        i = 0
        for village in landscape_villages:
            if i > 0:
                village_geojson += ','
            village_geojson += '{"type": "Feature", "properties": {"landscape": "%s", "survey": "%s", "village": "%s"}, "geometry": %s }' % \
                               (landscape_name, village.dataset_name, village.village, village.geojson)
            i += 1
    village_geojson += ']}'

    return village_geojson


def survey_villages(survey):
    """
    Return survey villages as GeoJSON
    :param survey:
    :return:
    """
    survey_villages = Answer.objects.raw("""SELECT row_number() OVER () as answer_id,
                                                dataset_name, 
                                                village, 
                                                ST_AsGeoJSON(ST_SetSRID(ST_MakePoint(avg(long), avg(lat)),4326)) as geojson 
                                            FROM bns_answer a 
                                                JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid 
                                                JOIN bns_answergps g ON a.answer_id = g.answer_id
                                            WHERE dataset_name = '{}' AND lat != 0 AND long != 0
                                            GROUP BY dataset_name, village""".format(survey))

    village_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(survey_villages):
        i = 0
        for village in survey_villages:
            if i > 0:
                village_geojson += ','
            village_geojson += '{"type": "Feature", "properties": {"survey": "%s", "village": "%s"}, "geometry": %s }' % \
                               (village.dataset_name, village.village, village.geojson)
            i += 1
    village_geojson += ']}'

    return village_geojson
