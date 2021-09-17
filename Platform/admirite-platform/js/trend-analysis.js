function resetCanvas() {
    $('#ta-chart').remove(); // this is my <canvas> element
    $('#chart-container').append('<canvas id="ta-chart" height="100px"></canvas>');
}

function line_chart_data(dataset) {
    /*
    Input: dataset -> 'drugs', 'markets', 'countries'
    */

    var res = null;

    var data_params = {
        "y": $('#ta-y option:selected').text()
    }

    var x_selection = $('#ta-x option:selected').text()
    if (x_selection === "Month") {
        data_params["year"] = $('#ta-year').text();
    } else if (x_selection === "Day") {
        data_params["year"] = $('#ta-year').text();
        data_params["month"] = $('#ta-month').text();
    }

    console.log(data_params)

    $.ajax({
        url: 'http://0.0.0.0:4500/ta/' + dataset + '/',
        type: 'GET',
        data: data_params,
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

function init_line_chart() {
    var ctx = document.getElementById("ta-chart");
    var ta_chart = new Chart(ctx, {
        type: 'line',
        options: {
            legend: {
                display: false,
            },
        }
    });
}

function set_line_chart(date, data) {
    datasets = []

    dataset_names = []
    $.each(data, function(key, val) {
        dataset_names.push(key)
    });


    dataset_values = {}
        // For each x-time, iterate over the dataset to retrieve such information 
    $.each(date, function(idx, time) {
        $.each(data, function(country, timestamps) {
            //console.log(key)
            // Each dataset must have an array of values with the same length of the x values 
            if (!dataset_values.hasOwnProperty(country)) {
                dataset_values[country] = Array(date.length).fill(0)
            }

            if (timestamps != null) {
                //console.log(dataset_values[key])
                dataset_values[country][idx] = timestamps[time]
            }
        });
    });

    datasets = []
    $.each(dataset_values, function(label, data) {
        var dataset = {
            data: data,
            label: label,
            backgroundColor: 'rgba(232, 245, 233, 0.5)',
            borderColor: '#2196F3',
            pointBackgroundColor: '#1976D2',
            borderWidth: 2
        }
        datasets.push(dataset)
    });

    // Set the line chart
    resetCanvas();
    var ctx = document.getElementById("ta-chart");
    var ta_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: date,
            datasets: datasets
        },
        options: {
            legend: {
                display: false,
            },
        }
    });
}


init_line_chart();

$(document).ready(function() {
    $('#ta-setting-form').submit(function(e) {
        //prevent Default functionality
        e.preventDefault();

        var data = line_chart_data("drugs");
        set_line_chart(data[0], data[1])
    });


});