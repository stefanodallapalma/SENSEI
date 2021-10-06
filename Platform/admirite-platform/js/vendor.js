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


jsonVendors = apiSearchVendors("");

$(document).ready(function() {
    var table = $('#example').dataTable();
    console.log(table);

    $.each(jsonVendors, function(idx, jsonVendor) {
        jsonVendor = JSON.parse(JSON.stringify(jsonVendor).replace(/\:null/gi, "\:\"\""));
        table.fnAddData([idx + 1, jsonVendor['name'], jsonVendor['market'], jsonVendor['country']]);
    });
});