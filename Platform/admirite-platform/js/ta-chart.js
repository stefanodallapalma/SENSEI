function setDatasetColors(data) {
    $.each(data, function(key, val) {
        setLineChartColor(key);
    });
}

function generateLineChartData(api_data) {
    /*
    Takes in input the ta data and generate a dict with key = dataset and value = y label
    */

    dataset_values = {}

    date = api_data[0]
    data = api_data[1]

    // For each x-time, iterate over the dataset to retrieve such information 
    $.each(date, function(idx, time) {
        $.each(data, function(country, timestamps) {
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

    return dataset_values;
}

function apiTAData(dataset, params) {
    /*
    Input: dataset -> 'drugs', 'markets', 'countries'
    */

    if (dataset.toLowerCase() == 'darkmarkets') {
        dataset = 'markets'
    }

    var res = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/ta/' + dataset.toLowerCase() + '/',
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

function addCheckboxDataset(id_ul, idx, dataset_name) {
    var hue = dataset_colors[dataset_name]['borderColor'];

    $('#' + id_ul).append('\
    <li style="display: inline-flex;">\
        <div id="dataset-checkbox-' + idx + '" class="form-check">\
            <label class="form-check-label">\
                <input class="form-check-input" type="checkbox" value="' + dataset_name + '">' + dataset_name + '\
            </label>\
        </div>\
        <div class="child" style="margin: 5px; background-color: ' + hue + ';"></div>\
    </li>');

}