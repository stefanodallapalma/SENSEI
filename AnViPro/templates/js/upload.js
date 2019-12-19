$(document).ready(function() {
    $("#dataZipFile").click(function() {
        alert("CLICK")
    });
    
    //$("#uploadForm").on('click', '#btn_zip_submit', function () {
    $("#btn_zip_submit").click(function() {
        alert("AAA");
        var fd = new FormData(); 
        var zipFile = $('#dataZipFile').val(); 
        fd.append('zipFile', zipFile); 
        alert(fd);

        $.ajax({
            //url: 'http://0.0.0.0:5000/upload',
            url: '/upload', 
            type: 'post', 
            data: fd, 
            contentType: false, 
            processData: false, 
            success: function(response){ 
                if(response != 0){ 
                   alert('file uploaded');
                } 
                else{ 
                    alert('file not uploaded'); 
                } 
            }, 
        }); 
    }); 
});