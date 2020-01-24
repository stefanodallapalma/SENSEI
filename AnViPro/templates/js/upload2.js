$(document).ready(function() {
    $("#btn_zip_submit").click(function() {
        var fd = new FormData($('#uploadForm')[0]); 
        //var zipFile = $('#dataZipFile').val(); 
        //fd.append('zipFile', zipFile);

        $.ajax({
            url: 'http://0.0.0.0:5000/load',
            //url: '/upload', 
            type: 'post', 
            data: fd, 
            contentType: false,
            cache: false, 
            processData: false, 
            success: function(response){ 
                alert("Success!"); 
            },
            
        });
    });

    $("#btn_add_page").click(function() {
        var page_block = $("#div_page_block").html();
        $("#page_section").append(page_block)
    });
});