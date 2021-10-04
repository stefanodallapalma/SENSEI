function apiVendorProducts(market = null) {
    var res = null;

    var params = null
    if (market != null && market != "All") {
        params = { "market": market }
    }

    $.ajax({
        url: 'http://0.0.0.0:4500/vendor/treemap/n-products/',
        type: 'GET',
        data: params,
        datatype: 'jsonp',
        success: function(data) {
            console.log("Line Chart Data");
            console.log(data);
            res = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return res;
}

function apiMarketList() {
    var marketList = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/market/list/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Market list");
            console.log(data);

            marketList = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return marketList;
}

function apiTreemapVendorInfo(vendor) {
    var vendorTreemapInfo = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/vendor/treemap/' + vendor,
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Vendor treemap info");
            console.log(data);

            vendorTreemapInfo = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return vendorTreemapInfo;
}

function initData(data) {
    var treemapData = []

    var header = {
        label: "Vendor's Treemap",
        value: null,
        color: '#B3FAFF'
    }

    treemapData.push(header);

    $.each(data, function(idx, elem) {
        var treemapElem = {
            label: idx,
            value: elem,
            parent: "Vendor's Treemap",
            data: {
                title: idx,
                description: "N. products: " + elem
            }
        }

        treemapData.push(treemapElem)
    });

    return treemapData;
}

function createTreemap(idMap, data, width = 900, height = 600) {
    $('#' + idMap).jqxTreeMap({
        width: width,
        height: height,
        headerHeight: 0,
        source: data,
        colorRange: 100,
        renderCallbacks: {
            '*': function(element, value) {
                element.click(function() {
                    console.log("Label:", value["label"]);
                    var info = apiTreemapVendorInfo(value["label"]);
                    console.log(info);

                    $('#vendor-info-container').empty();

                    var first = true;

                    var totProd = 0;
                    $.each(info, function(key, value) {
                        totProd += value;
                    });

                    console.log(totProd);

                    $.each(info, function(key, value) {
                        addInfoToHtml(key, value, totProd, first);
                        first = false;
                    });
                });

                if (value.data) {
                    element.jqxTooltip({
                        content: '<div><div style="font-weight: bold; max-width: 200px; font-family: verdana; font-size: 13px;">' + value.data.title + '</div><div style="width: 200px; font-family: verdana; font-size: 12px;">' + value.data.description + '</div></div>',
                        position: 'mouse',
                        autoHideDelay: 6000
                    });
                } else if (value.data === undefined) {
                    element.css({
                        backgroundColor: '#fff',
                        border: '1px solid #555'
                    });
                }
            }
        }
    });
}

function addInfoToHtml(name, value, maxValue = 12, top = false) {
    name = name.replaceAll("/", "-");
    name = name.replaceAll(" ", "-");

    var mTop = "mT-15"
    if (top == true) {
        mTop = "mT-25"
    }

    var div = '<div class="layer w-100 ' + mTop + '">\
    <h5 id="' + name + '" class="mB-5">' + name.replaceAll("-", " ") + '</h5>\
    <small id="' + name + '" class="fw-600 c-grey-700">N. products: ' + value + '</small>\
    <span id="' + name + '-percentage" class="pull-right c-grey-600 fsz-sm"></span>\
    <div class="progress mT-10">\
    <div id="' + name + '-percentage-bar" class="progress-bar bgc-deep-purple-500" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">50% Complete</span></div>\
    </div></div>'

    $('#vendor-info-container').append(div);

    var percentage = ((value / maxValue) * 100).toFixed(2);
    $('#' + name + '-percentage').text(percentage + "%");
    $('#' + name + '-percentage-bar').attr('aria-valuenow', "" + percentage);
    $('#' + name + '-percentage-bar').css('width', percentage + "%");
}

$(document).ready(function() {
    var apiData = apiVendorProducts();
    var data = initData(apiData);

    var markets = apiMarketList();

    // Set markets drop-down list
    $('#tm-markets').empty();
    $('#tm-markets').append($('<option>', {
        value: 0,
        text: 'All'
    }));
    $.each(markets, function(idx, market) {
        $('#tm-markets').append($('<option>', {
            value: idx + 1,
            text: market
        }));
    });

    createTreemap('treemap', data);

    $('#tm-markets').on('change', function(e) {
        market = $('#tm-markets option:selected').text();

        var marketData = apiVendorProducts(market);
        console.log(marketData);
        data = initData(marketData);

        createTreemap('treemap', data);
    });


});