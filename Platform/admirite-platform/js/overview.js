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

function addTopVendor(vendor, qty, price) {
    //return "<tr><td class=\"fw-600\">" + vendor + "</td<td><span class=\"badge bgc-red-50 c-red-700 p-10 lh-0 tt-c rounded-pill\">AAA</span></td><td>" + qty + "</td><td><span class=\"text-success\">" + price + "</span></td></tr>"
    return "<tr>" +
        "<td class=\"fw-600\">" + vendor + "</td>" +
        "<td>" + qty + "</td>" +
        "<td><span class=\"text-success\">€" + price + "</span></td>" +
        "</tr>"
}

function getVendorsReport() {
    $.ajax({
        url: 'http://0.0.0.0:4500/top-vendors/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            $("#top-vendors-body").empty();
            console.log("TOP VENDORS");
            console.log(data);

            var date = data["date"]
            $('#top-vendors-date').text(date)

            var tot_price = data["price"].toString();
            var parts = tot_price.match(/.{1,3}/g);
            var new_value = parts.join("ॱ");
            $('#top-vendors-sum-price').text("€ " + new_value)

            for (var i = 0; i < data["top_vendors"].length; i++) {
                console.log(data["top_vendors"][i])
                var vendor = data["top_vendors"][i]['vendor']
                var qty = data["top_vendors"][i]['qty']
                var price = data["top_vendors"][i]['tot_price']

                var html_row = addTopVendor(vendor, qty, price)
                console.log(html_row)
                $(html_row).appendTo($("#top-vendors-body"))
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

function getCountryList() {
    $.ajax({
        url: 'http://0.0.0.0:4500/country/list/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Country list");
            console.log(data);

            for (var i = 0; i < data.length; i++) {
                $('#counntrySelection').append($('<option>', {
                    value: i + 1,
                    text: data[i]
                }));
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

function getRawData() {
    $.ajax({
        url: 'http://0.0.0.0:4500/country/rawdata/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Raw Data");
            console.log(data);

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
    getVendorsReport();
    getRawData();
    getCountryList();
});