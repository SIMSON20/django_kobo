    function map_init(map, options) {


        var surveys = [{% for survey in surveys %}'{{ survey.dataset_name }}', {% endfor %}];

        var colors = randomColor({
           count: surveys.length,
           hue: 'blue'
        });

        var survey_colors = {}

        for (i = 0; i < surveys.length; i++) {
            survey_colors[surveys[i]] = colors[i];

        }


        var geojsonMarkerOptions = {
            radius: 5,

            color: "darkblue",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8};

        var v_geojson = {{ village_geojson|safe }};
        var l_geojson = {{ landscape_geojson|safe }};



        var l_layer = L.geoJSON( l_geojson ).addTo(map);



        var v_layer = L.geoJSON( v_geojson ,{
                                        pointToLayer: function (feature, latlng) {
                                            return L.circleMarker(latlng, geojsonMarkerOptions);
                                        }, style: function (feature){return {'color': survey_colors[feature.properties.survey]}}
                                    }).addTo(map);

        map.fitBounds(v_layer.getBounds());
        map.fitBounds(l_layer.getBounds());


        var legend = L.control({position: 'bottomright'});
            legend.onAdd = function (map) {

            var div = L.DomUtil.create('div', 'info legend');
            labels = ['<strong>Surveys</strong>'];

            for (var i = 0; i < surveys.length; i++) {

                    div.innerHTML +=
                    labels.push(
                        '<i class="circle" style="background:' + colors[i] + '"></i>' +
                    (surveys[i] ? surveys[i] : '+'));

                }
                div.innerHTML = labels.join('<br>');
            return div;
            };
            legend.addTo(map);

    }