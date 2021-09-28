function initYearDatepicker() {
    $('.date-picker').datepicker({
        changeYear: true,
        yearRange: "1970:+0",
        showButtonPanel: true,
        stepMonths: 12,
        dateFormat: 'yy',
        onClose: function(dateText, inst) {
            console.log(inst.selectedYear)
            $(this).datepicker('setDate', new Date(inst.selectedYear, 1));
        }
    });

    $(".date-picker").focus(function() {
        $(".ui-datepicker-month").hide();
    });
}

function initMonthYearDatepicker() {
    $('.date-picker').datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "1970:+0",
        showButtonPanel: true,
        dateFormat: 'MM yy',
        onClose: function(dateText, inst) {
            $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
        }
    });

    $(".date-picker").focus(function() {
        $(".ui-datepicker-month").show();
    });
}

$(document).ready(function() {
    $('#datepicker-container').hide();

    $('#ta-x').change(function() {
        var x = $('#ta-x option:selected').text();

        $(".date-picker").datepicker('setDate', null);
        $(".date-picker").datepicker("destroy");

        if (x === "Year") {
            $('#datepicker-container').hide();
        } else {
            $('#datepicker-container').show();

            if (x === "Month") {
                initYearDatepicker();
            } else {
                initMonthYearDatepicker();
            }
        }
    });

    $('#cp-x').change(function() {
        var x = $('#cp-x option:selected').text();

        $(".date-picker").datepicker('setDate', null);
        $(".date-picker").datepicker("destroy");

        if (x === "Year") {
            $('#datepicker-container').hide();
        } else {
            $('#datepicker-container').show();

            if (x === "Month") {
                initYearDatepicker();
            } else {
                initMonthYearDatepicker();
            }
        }
    });
});