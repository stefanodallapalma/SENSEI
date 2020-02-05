$(document).ready(function() {
    $("#btn_zip_submit").click(function() {
        var fd = new FormData($('#ta_load_data_form')[0]);
        $.ajax({
            url: 'http://0.0.0.0:5000/v1/data/load-marketplace',
            type: 'post',
            data: fd,
            contentType: false,
            cache: false,
            processData: false
        }).done(function (response) {
            alert("Success!");
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(textStatus);
            alert(errorThrown);
        });
    });

    $("#btn_sq_newres").click(function() {
        var fd = new FormData($('#sq_new_load_data_form')[0]);
        $.ajax({
            url: 'http://0.0.0.0:5000/v1/data/load-html-files',
            type: 'post',
            data: fd,
            contentType: false,
            cache: false,
            processData: false
        }).done(function (response) {
            alert("Success!");
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(textStatus);
            alert(errorThrown);
        });
    });

    $("#btn_sq_res").click(function() {
        var fd = new FormData($('#sq_load_data_form')[0]);
        $.ajax({
            url: 'http://0.0.0.0:5000/v1/data/load-html-files',
            type: 'post',
            data: fd,
            contentType: false,
            cache: false,
            processData: false
        }).done(function (response) {
            alert("Success!");
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(textStatus);
            alert(errorThrown);
        });
    });



});