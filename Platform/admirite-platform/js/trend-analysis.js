function getTAParams() {
    var data_params = {
        "y": $('#ta-y option:selected').text()
    }

    var x_selection = $('#ta-x option:selected').text()

    var date = $(".date-picker").val();
    console.log(date)
    if (x_selection === "Month") {
        data_params["year"] = date;
    } else if (x_selection === "Day") {
        date = date.split(" ");
        data_params["year"] = date[1];
        data_params["month"] = date[0];
    }

    return data_params
}


$('#dataset-section').hide();
initEmptyLineChart('ta-chart');

$(document).ready(function() {
    $('#ta-setting-form').submit(function(e) {
        //prevent Default functionality
        e.preventDefault();

        // API Params
        var dataset = $('#ta-dataset option:selected').text();
        var params = getTAParams();

        // Retrieve ta data
        var data = apiTAData(dataset, params);
        var lineChartData = generateLineChartData(data);
        var datasetChartIndex = {}

        // Save the index of each dataset
        var i = 0;
        $.each(lineChartData, function(dataset, values) {
            datasetChartIndex[dataset] = i
            i += 1;
        });

        // Set the colors of the dataset on the line chart
        $.each(lineChartData, function(key, val) {
            setLineChartColor(key);
        });

        var chart = setNLineChart('ta-chart', 'chart-container', data[0], lineChartData, '100px');

        //var chart = set_line_chart(data[0], data[1]);

        // Update dataset checkbox
        $('#dataset-section').show();
        $('.dataset-checkboxes').empty();

        var idx = 0
        $.each(lineChartData, function(key, val) {
            addCheckboxDataset('dataset-checkboxes', idx, key);
            idx += 1;
        });

        $('.form-check-input').prop('checked', true);

        console.log(datasetChartIndex);
        console.log("Form Check")
        $(".form-check-input").click(function() {
            var dataset = this.value;
            console.log(dataset);
            var idx = datasetChartIndex[dataset]
            console.log(idx);

            if (this.checked == false) {
                chart.getDatasetMeta(idx).hidden = true;
            } else {
                chart.getDatasetMeta(idx).hidden = false;
            }

            chart.update();
        });
    });
});