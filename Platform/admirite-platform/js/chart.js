colors = [{
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(33, 150, 243)', // blue 500
        pointBackgroundColor: 'rgb(25, 118, 210)' // blue 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(156, 39, 176)', // purple 500
        pointBackgroundColor: 'rgb(123, 31, 162)' // purple 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(255, 235, 59)', // yellow 500
        pointBackgroundColor: 'rgb(251, 192, 45)' // yellow 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(76, 175, 80)', // green 500
        pointBackgroundColor: 'rgb(56, 142, 60)' // green 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(244, 67, 54)', // red 500
        pointBackgroundColor: 'rgb(211, 47, 47)' // red 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(255, 152, 0)', // orange 500
        pointBackgroundColor: 'rgb(245, 124, 0)' // orange 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(255, 87, 34)', // deep orange 500
        pointBackgroundColor: 'rgb(230, 74, 25)' // deep orange 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(96, 125, 139)', // blue grey 500
        pointBackgroundColor: 'rgb(69, 90, 100)' // blue grey 700
    },
    {
        backgroundColor: 'rgba(232, 245, 233, 0.5)',
        borderColor: 'rgb(63, 81, 181)', // indigo 500
        pointBackgroundColor: 'rgb(25, 118, 210)' // indigo 700
    }
];

function resetCanvas(id, id_container = null, height = '100px') {
    $('#' + id).remove(); // this is my <canvas> element
    $('#' + id_container).append('<canvas id="' + id + '" height="' + height + ' !important"></canvas>');
}

function initEmptyLineChart(id, display = false) {
    var ctx = document.getElementById(id);
    var new_chart = new Chart(ctx, {
        type: 'line',
        options: {
            maintainAspectRatio: true,
            spanGaps: true,
            legend: {
                display: display,
            },
        }
    });

    return new_chart;
}

function setNLineChart(id_canvas, id_container, x, data, height = '100px') {
    datasets = []
    $.each(data, function(label, data) {
        var color = getLineChartColor(label)
        var dataset = {
            data: data,
            label: label,
            backgroundColor: color['backgroundColor'],
            borderColor: color['borderColor'],
            pointBackgroundColor: color['pointBackgroundColor'],
            borderWidth: 2
        }
        datasets.push(dataset)
    });

    // Set the line chart
    resetCanvas(id_canvas, id_container, height);

    var ctx = document.getElementById(id_canvas);
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x,
            datasets: datasets
        },
        options: {
            maintainAspectRatio: true,
            spanGaps: true,
            legend: {
                display: false,
            },
        }
    });

    return chart;
}

function getLineChartColor(dataset) {
    if (!dataset_colors.hasOwnProperty(dataset)) {
        setLineChartColor(dataset);
    }

    return dataset_colors[dataset];
}

function setLineChartColor(dataset) {
    if (!dataset_colors.hasOwnProperty(dataset)) {
        dataset_colors[dataset] = {
            backgroundColor: colors[i % colors.length]['backgroundColor'],
            borderColor: colors[i % colors.length]['borderColor'],
            pointBackgroundColor: colors[i % colors.length]['pointBackgroundColor']
        }
        i += 1;
    }
}

var i = 0
var dataset_colors = []