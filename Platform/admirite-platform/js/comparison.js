function getCPParams() {
    var x = $('#cp-x option:selected').text();
    var y = $('#cp-y option:selected').text();

    var data_params = {
        "y": y
    }

    var date = $(".date-picker").val();

    if (x === "Month") {
        data_params["year"] = date;
    } else if (x === "Day") {
        date = date.split(" ");
        data_params["year"] = date[1];
        data_params["month"] = date[0];
    }

    return data_params;
}

function getCountryList() {
    var countryList = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/country/list/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Country list");
            console.log(data);

            countryList = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return countryList;
}

function updateCheckboxes() {
    $('#dataset-section').show();
    $('.dataset-checkboxes').empty();

    var idx = 0
    $.each(datasetChartsIndex, function(key, val) {
        addCheckboxDataset('dataset-checkboxes', idx, key);
        idx += 1;
    });

    $('.form-check-input').prop('checked', true);

    // Checkbox interaction
    if (charts != null && charts.length == 2) {
        $(".form-check-input").click(function() {
            var dataset = this.value;

            var idxChart0 = datasetChartsIndex[dataset][0];
            var idxChart1 = datasetChartsIndex[dataset][1];

            if (idxChart0 != null) console.log(charts[0].getDatasetMeta(idxChart0));
            if (idxChart1 != null) console.log(charts[1].getDatasetMeta(idxChart1));

            if (this.checked == false) {
                if (idxChart0 != null) charts[0].getDatasetMeta(idxChart0).hidden = true;
                if (idxChart1 != null) charts[1].getDatasetMeta(idxChart1).hidden = true;
            } else {
                if (idxChart0 != null) charts[0].getDatasetMeta(idxChart0).hidden = false;
                if (idxChart1 != null) charts[1].getDatasetMeta(idxChart1).hidden = false;
            }

            charts[0].update();
            charts[1].update();
        });
    }
}

function updateDatasetChartIndexes(idChart, lineChartData) {
    var i = 0;
    $.each(lineChartData, function(dataset, values) {
        if (!datasetChartsIndex.hasOwnProperty(dataset)) {
            datasetChartsIndex[dataset] = Array(2);
        }

        datasetChartsIndex[dataset][idChart] = i
        i += 1;
    });
}


var countries_cache = {};
var params = null;
var dataset = null;
var datasetChartsIndex = {};
var charts = [];

$('#dataset-section').hide();
initEmptyLineChart('cp-chart-1');
initEmptyLineChart('cp-chart-2');


$(document).ready(function() {
    // Country list (sync)
    var countries = getCountryList()

    // Set countries drop-down list
    $.each(countries, function(idx, country) {
        $('#cp-l-countries').append($('<option>', {
            value: idx + 1,
            text: country
        }));

        $('#cp-r-countries').append($('<option>', {
            value: idx + 1,
            text: country
        }));
    });

    // Setting form
    $('#cp-setting-form').submit(function(e) {
        //prevent Default functionality
        e.preventDefault();

        params = getCPParams();
        var countries_params = [$('#cp-l-countries option:selected').text(), $('#cp-r-countries option:selected').text()];
        dataset = $('#cp-dataset option:selected').text();

        charts = []
        datasetChartsIndex = {}

        $.each(countries_params, function(idx, country) {
            params['country'] = country

            // API TA call
            var data = apiTAData(dataset, params);
            var lineChartData = generateLineChartData(data);

            console.log(lineChartData);

            // Save the index of each dataset
            updateDatasetChartIndexes(idx, lineChartData);

            // Set the colors of the dataset on the line chart
            $.each(lineChartData, function(key, val) {
                setLineChartColor(key);
            });

            // Generate the chart
            var idChart = "cp-chart-" + (idx + 1)
            var chart = setNLineChart(idChart, 'chart-container-' + (idx + 1), data[0], lineChartData, '150px');
            charts.push(chart);
        });

        delete params['country'];

        // Update dataset checkbox
        updateCheckboxes();
    });

    // Country drop down on change event
    $('#cp-l-countries').on('change', function(e) {
        var newCountry = $('#cp-l-countries option:selected').text();
        console.log(newCountry)
        if (params != null) {
            params['country'] = newCountry

            // API TA call
            var data = apiTAData(dataset, params);
            delete params['country']
            var lineChartData = generateLineChartData(data);

            updateDatasetChartIndexes(0, lineChartData);

            // Set the colors of the dataset on the line chart
            $.each(lineChartData, function(key, val) {
                setLineChartColor(key);
            });

            // Generate the chart
            var chart = setNLineChart("cp-chart-1", 'chart-container-1', data[0], lineChartData, '150px');
            charts[0] = chart;

            // Update dataset checkbox
            updateCheckboxes();
        }
    });

    $('#cp-r-countries').on('change', function(e) {
        var newCountry = $('#cp-r-countries option:selected').text();
        console.log(newCountry)
        if (params != null) {
            params['country'] = newCountry

            // API TA call
            var data = apiTAData(dataset, params);
            delete params['country']
            var lineChartData = generateLineChartData(data);

            updateDatasetChartIndexes(1, lineChartData);

            // Set the colors of the dataset on the line chart
            $.each(lineChartData, function(key, val) {
                setLineChartColor(key);
            });

            // Generate the chart
            var chart = setNLineChart("cp-chart-2", 'chart-container-2', data[0], lineChartData, '150px');
            charts[1] = chart;

            // Update dataset checkbox
            updateCheckboxes();
        }
    });
});