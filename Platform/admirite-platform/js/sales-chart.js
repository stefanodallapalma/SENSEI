function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

function getChartSalesData() {
    var sales = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/sales/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Sales");
            console.log(data);

            sales = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return sales;
}

$(document).ready(function() {
    // Our labels along the x-axis
    // TO DO: MONTH CHECKING TO KNOW THE N. OF DAYS 
    var sales_data = getChartSalesData();

    var days = [];
    var sales = [];
    for (var day in sales_data) {
        days.push(day);
        sales.push(sales_data[day])
    }

    console.log(days)
    console.log(sales)
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: sales,
                label: "Sales",
                backgroundColor: 'rgba(232, 245, 233, 0.5)',
                borderColor: '#2196F3',
                pointBackgroundColor: '#1976D2',
                borderWidth: 2
            }]
        },
        options: {
            legend: {
                display: false,
            },
        }
    });

});