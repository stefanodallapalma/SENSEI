function apiSearchVendors(vendor_query) {
    var res = null;

    var params = null;
    if (vendor_query != null) {
        params = { "vendor-name": vendor_query }
    }

    $.ajax({
        url: 'http://0.0.0.0:4500/vendor/search',
        type: 'GET',
        data: params,
        datatype: 'jsonp',
        success: function(data) {
            console.log("Vendor List");
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

function apiGetVendorInfo(vendor_name, market) {
    var res = null;

    var params = null;
    if (vendor_name == null || market == null) {
        return null
    }

    params = { "market": market }

    $.ajax({
        url: 'http://0.0.0.0:4500/vendor/info/' + vendor_name,
        type: 'GET',
        data: params,
        datatype: 'jsonp',
        success: function(data) {
            console.log("Vendor Info");
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

jsonVendors = apiSearchVendors("");
$('#vendor_info_container').hide();

$(document).ready(function() {
    var table = $('#example').dataTable();
    console.log(table);

    $.each(jsonVendors, function(idx, jsonVendor) {
        jsonVendor = JSON.parse(JSON.stringify(jsonVendor).replace(/\:null/gi, "\:\"\""));
        table.fnAddData([idx + 1, jsonVendor['name'], jsonVendor['market'], jsonVendor['country']]);
    });

    $('#vendor-table-body').on('click', 'tr', function() {
        var lis = $(this).find("td");
        var vendor = $(lis[1]).text();
        var market = $(lis[2]).text();

        $('#vendor_info').empty();
        $('#vendor_info_container').show();

        // Get vendor info
        var vendor_info = apiGetVendorInfo(vendor, market);
        var first = true;
        $.each(vendor_info, function(key, val) {
            if (val == null) {
                val = "";
            }
            if (first == true) {
                $('#vendor_info').append('<h6 class="mT-50">' + key + ': ' + '<small>' + val + '</small>' + '</h6>');
                first = false;
            } else {
                $('#vendor_info').append('<h6 class="mT-20">' + key + ': ' + '<small>' + val + '</small>' + '</h6>')
            }

        });
    });
});