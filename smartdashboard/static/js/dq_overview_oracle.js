var cdr_types = ["com", "vou", "cm", "adj", "first", "mon", "data", "voice", "sms", "clr"];
var lines_oracle = [];
var oracle_variance_chart = null;

$('#min_oracle').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_hive').val() ? jQuery('#max_hive').val() : false
        })
    }
});

$('#max_oracle').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_oracle').val() ? jQuery('#min_oracle').val() : false
        })
    }
});

$("#search_date_oracle").click(function () {
    if ($("#search_date_hive")[0].checkValidity()) {
        var start_date = $("#min_oracle").val();
        var end_date = $("#max_oracle").val();
        var period = $("#period_oracle").val();
        if (start_date != "" && end_date != "" && period != "") {
            update_data_oracle(start_date, end_date, period);
        }
        else {
            alert("Form is not completed.")
        }
    }
    else {
        $("#search_date_hive")[0].reportValidity();
    }
});

function push_lines_oracle(cdr, data_cdr) {
    lines_oracle.push({
        name: cdr + ' variance',
        data: data_cdr,
        type: 'line'
    });
}

function update_data_oracle(start_date, end_date, period) {
    $.ajax({
        url: "/dqchecks_overview_oracle_js",
        method: "POST",
        dataType: "json",
        data: {
            "start_date": start_date,
            "end_date": end_date,
            "period": period
        }
    }).done(function (data) {
        lines_oracle = [];
        for (c of cdr_types) {
            var variance = "variance_" + c;
            var data_cdr = data[variance]
            push_lines_oracle(c, data_cdr);
        }
        oracle_variance_chart.updateOptions({
            xaxis: {
                categories: data["date_list"],
            }
        }
        );
        oracle_variance_chart.updateSeries(lines_oracle);
    });
}

$.ajax({
    url: "/dqchecks_overview_oracle_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    for (c of cdr_types) {
        var variance = "variance_" + c;
        var data_cdr = data[variance]
        push_lines_oracle(c, data_cdr);
    }
    var options = {
        series: lines_oracle,
        chart: {
            type: 'line',
            height: 350
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '55%',
                endingShape: 'rounded'
            },
        },
        colors: ["#2979FF", "#90CAF9", "#C5E1A5", "#AA00FF", "#CE93D8", "#4E342E", "#FFC107", "#A1887F", "#76FF03", "#546E7A"],
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            curve: 'smooth',
        },
        xaxis: {
            categories: data["date_list"],
        },
        fill: {
            opacity: 1
        },
        markers: {
            size: 3
        },
    };
    oracle_variance_chart = new ApexCharts(document.querySelector("#variances_oracle"), options);
    oracle_variance_chart.render();
});

// $('#oracle_table').DataTable({
//     ajax: '/dqchecks_oracle_table'
// });

$(document).ready(function() {
    $('#oracle_table').DataTable();
} );