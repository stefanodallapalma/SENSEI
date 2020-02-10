$(document).ready(function() {
    $.ajax({
        url: 'http://0.0.0.0:5000/resource/get_html_folders',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        cache: false,
        processData: false,
        async:true
    }).done(function (response) {
        if (response.length == 0) {
            $("#resource_folders_list").css("display", "none")
            $("#add_pages_block").append($("<label>: no projects found</label>"))
            $("#btn_sq_res").attr("disabled", true);
        } else {
            for (var i = 0; i < response.length; i++) {
                var value = response[i]
                $('#resource_folders_list').append($("<option></option>").attr("value",value).
                attr("id", "resource_folder_id").text(value));
            }
            $("#btn_sq_res").attr("disabled", false);
        }

    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        alert("Status code: " + XMLHttpRequest.status + "\nStatus text: " + XMLHttpRequest.status +
        "\nOn ready state change: " + XMLHttpRequest.onreadystatechange +
        "\nReady State: " + XMLHttpRequest.readyState);
        alert(textStatus);
        alert(errorThrown);
    });

    $('#sq_loadData_radio').click(function() {
        $('#load_div').css("display", "block")
        $('#delete_div').css("display", "none")
    });

    $('#sq_deleteData_radio').click(function() {
        $('#load_div').css("display", "none")
        $('#delete_div').css("display", "block")
    });

    $("#btn_add_page").click(function() {
        var page_block = $("#div_page_block").html();
        $("#page_section").append(page_block)
    });

    // Listen for click on toggle checkbox
    $('#select-all').click(function(event) {
        if(this.checked) {
            // Iterate each checkbox
            $(':checkbox').each(function() {
                this.checked = true;
            });
        } else {
            $(':checkbox').each(function() {
                this.checked = false;
            });
        }
    });
});