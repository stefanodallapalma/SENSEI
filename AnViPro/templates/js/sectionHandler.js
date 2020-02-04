$(document).ready(function() {

    $('#new_resource_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: 'http://0.0.0.0:5000/resource/get_html_folders',
            type: 'post',
            contentType: 'application/json',
            dataType: 'json',
            cache: false,
            processData: false
            /*success: function(data){
                alert("success");
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(textStatus);
                alert(errorThrown);
            }*/
        }).done(function (response) {
            alert("success");
        }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status code: " + XMLHttpRequest.status + "\nStatus text: " + XMLHttpRequest.status + "\nOn ready state change: " + XMLHttpRequest.onreadystatechange + "\nReady State: " + XMLHttpRequest.readyState);
            alert(textStatus);
            alert(errorThrown);
        });

    });


    $('#sq_loadData_radio').click(function() {
        $('#load_div').css("display", "block")
        $('#delete_div').css("display", "none")
    });

    $('#sq_deleteData_radio').click(function() {
        $('#load_div').css("display", "none")
        $('#delete_div').css("display", "block")
    });
});