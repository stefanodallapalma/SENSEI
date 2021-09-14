function getTopInsights() {
    $.ajax({
        url: 'http://0.0.0.0:4500/insights/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log(data)
            var n_markets = data["n_markets"]
            var n_vendors = data["n_vendors"]
            var n_products = data["n_products"]
            var n_reviews = data["n_reviews"]

            $('#n_markets').text(n_markets)
            $('#n_vendors').text(n_vendors)
            $('#n_products').text(n_products)
            $('#n_reviews').text(n_reviews)
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        }
    });
}

function getTopSales() {
    $.ajax({
        url: 'http://0.0.0.0:4500/country/top-sales/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("TOP SALES");
            console.log(data);
            for (var i = 0; i < data.length; i++) {
                var country = data[i]["country"];
                var n_products = data[i]["n_products"];
                var percentage = data[i]["percentage"];

                $('#top4-sales-' + (i + 1)).text(n_products);
                $('#top4-country-' + (i + 1)).text(country);
                $('#top4-percentage-' + (i + 1)).text(percentage + "%");
                $('#top4-percentage-bar-' + (i + 1)).attr('aria-valuenow', "" + percentage);
                $('#top4-percentage-bar-' + (i + 1)).css('width', percentage + "%");
            }

        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        }
    });
}

$(document).ready(function() {
    getTopInsights();
    getTopSales();
});