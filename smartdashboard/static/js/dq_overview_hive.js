var cdr_types = ["com", "vou", "cm", "adj", "first", "mon", "data", "voice", "sms", "clr"];
var lines_hive = [];
var hive_variance_chart = null;

$('#min_hive').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_hive').val() ? jQuery('#max_hive').val() : false
        })
    }
});

$('#max_hive').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_hive').val() ? jQuery('#min_hive').val() : false
        })
    }
});

$("#hive_overview_form").submit(function (event) {
    event.preventDefault();
    var start_date = $("#min_hive").val();
    var end_date = $("#max_hive").val();
    var period = $("#period_hive").val();
    update_data_hive(start_date,end_date,period);
});

function update_data_hive(start_date,end_date,period) {
    $.ajax({
        url: "/dqchecks_overview_hive_js",
        method: "POST",
        dataType: "json",
        data: { "start_date": start_date,
                "end_date": end_date,
                "period": period }
    }).done(function (data) {
        lines_hive = [];
        console.log(data);
        for (c of cdr_types) {
            var variance = "variance_" + c;
            lines_hive.push({
                name: c + ' variance',
                data: data[variance],
                type: 'line'
            });
        }
        hive_variance_chart.updateOptions({
            xaxis: {
                categories: data["date_list"],
            }
        }
        );
        hive_variance_chart.updateSeries(lines_hive);
    });
}

$.ajax({
    url: "/dqchecks_overview_hive_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    for (c of cdr_types) {
        var variance = "variance_" + c;
        lines_hive.push({
            name: c + ' variance',
            data: data[variance],
            type: 'line'
        });
    }
    var options = {
        series: lines_hive,
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
        colors: ['#77B6EA', '#84FFFF', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E", "#FFCDD2"],
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
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
    hive_variance_chart = new ApexCharts(document.querySelector("#variances_hive"), options);
    hive_variance_chart.render();
});