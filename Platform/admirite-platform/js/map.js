import { coordCountries } from './coordinates.js'

function getCountryAlpha2Code(country) {
    var alpha2Code = null;

    $.ajax({
        url: 'https://restcountries.eu/rest/v2/name/' + country,
        type: 'GET',
        datatype: 'json',
        success: function(data) {
            // First checj - Name
            for (var i = 0; i < data.length; i++) {
                console.log(data[i])
                if (data[i]["name"].toLowerCase() == country.toLowerCase()) {
                    alpha2Code = data[i]["alpha2Code"];
                    break;
                }
            }

            // Second check - Native name
            for (var i = 0; i < data.length; i++) {
                if (data[i]["nativeName"].toLowerCase() == country.toLowerCase()) {
                    alpha2Code = data[i]["alpha2Code"];
                    break;
                }
            }

            // Third check - Substring
            if (alpha2Code == null) {
                for (var i = 0; i < data.length; i++) {
                    if (data[i]["name"].toLowerCase().includes(country.toLowerCase())) {
                        alpha2Code = data[i]["alpha2Code"];
                        break;
                    }
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

function getCountryName(code) {
    var mapObject = $('#world-map').vectorMap('get', 'mapObject');
    var name = null;
    try {
        name = mapObject.getRegionName(code);
    } catch (err) {
        console.log(code + " reference not found");
    }

    return name;
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
                console.log(country)
                var alpha2Code = getCountryAlpha2Code(country)
                console.log(alpha2Code)

                if (alpha2Code != null) {
                    var name = getCountryName(alpha2Code)

                    if (name != null) {
                        // Add country on the map
                        addRegion(alpha2Code)

                        // Add marker on the map
                        var coord = coordCountries[alpha2Code]["coords"]
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


                }
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