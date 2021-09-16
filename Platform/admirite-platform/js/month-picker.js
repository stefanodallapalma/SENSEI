$('.month').hide()
$('.year').hide()

$(document).ready(function() {
    $('.date-picker').each(function() {
        var $datepicker = $(this),
            cur_date = ($datepicker.data('date') ? moment($datepicker.data('date'), "YYYY/MM/dd") : moment());

        function updateDisplay(cur_date) {
            $('#dateinput').val(cur_date);

            $datepicker.find('.date-container > .date > .text').text(cur_date.format('Do'));
            $datepicker.find('.date-container > .month > .text').text(cur_date.format('MMMM'));
            $datepicker.find('.date-container > .year > .text').text(cur_date.format('YYYY'));
            $datepicker.data('date', cur_date.format('YYYY/MM/DD'));
        }

        updateDisplay(moment());

        $datepicker.on('click', '[data-toggle="datepicker"]', function(event) {
            event.preventDefault();

            var cur_date = moment($(this).closest('.date-picker').data('date'), "YYYY/MM/DD"),
                type = ($(this).data('type') ? $(this).data('type') : "date"),
                method = ($(this).data('method') ? $(this).data('method') : "add"),
                amt = ($(this).data('amt') ? $(this).data('amt') : 1);

            if (method == "add") {
                var duration = moment.duration(1, type);
                cur_date = cur_date.add(duration);
            } else if (method == "subtract") {
                cur_date = cur_date.subtract(1, type);
            }

            updateDisplay(cur_date);
        });
    });

    $('#ta-x').change(function() {
        var time_category = $('#ta-x option:selected').text();

        if (time_category === "Year") {
            $('.month').hide()
            $('.year').hide()
        } else if (time_category === "Month") {
            $('.month').hide()
            $('.year').show()
        } else {
            $('.month').show()
            $('.year').show()
        }
    });

});