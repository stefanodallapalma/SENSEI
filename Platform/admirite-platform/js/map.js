import { coordCountries } from './coordinates.js'

function getCountryAlpha2Code(country) {
    var alpha2Code = null;

    $.ajax({
        url: 'https://restcountries.eu/rest/v2/name/' + country,
        type: 'GET',
        datatype: 'json',
        success: function(data) {
            // Remove general EU products
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                console.log(data[0])
                console.log(data[i])
                if (data[i]["name"] == country) {
                    alpha2Code = data[i]["alpha2Code"];
                    break;
                }
            }

        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("Restcountries API connection failed")
        },
        async: false
    });

    return alpha2Code;
}

function addMarkers(country) {
    var mapObject = $('#world-map').vectorMap('get', 'mapObject');
    mapObject.addMarkers(country);
}

function addRegion(region) {
    var mapObject = $('#world-map').vectorMap('get', 'mapObject');
    mapObject.setSelectedRegions(region);
}

$(document).ready(function() {
    console.log(coordCountries)
    $('#world-map').vectorMap({
        map: 'world_mill',
        backgroundColor: 'white',
        series: {
            regions: [{
                attribute: 'fill'
            }]
        },
        regionStyle: {
            initial: {
                fill: '#e4ecef',
                "fill-opacity": 1,
                stroke: 'none',
                "stroke-width": 0,
                "stroke-opacity": 1
            },
            hover: {
                "fill-opacity": 0.8,
                cursor: 'pointer'
            },
            selected: {
                fill: '#03a8f2'
            },
            selectedHover: {}
        }

    });

    $.ajax({
        url: 'http://0.0.0.0:4500/country/sales/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            // Remove general EU products
            delete data["EU (exact location unknown)"]

            var markers = []

            // Change the color in the overview map
            for (var country in data) {
                var alpha2Code = getCountryAlpha2Code(country)
                addRegion(alpha2Code)
                console.log(alpha2Code)

                var coord = coordCountries[alpha2Code]["coords"]
                console.log(coord)
                var n_sales = data[country]
                var label = country + " - " + n_sales
                console.log(label)

                var marker = {
                    latLng: coord,
                    name: label
                };

                markers.push(marker)


                addMarkers(markers)

            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        }
    });

});