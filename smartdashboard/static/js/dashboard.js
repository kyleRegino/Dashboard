var cdr_types = ["com", "vou", "cm", "adj", "first", "mon"];

var series_hive = [];
var series_oracle = [];

$.ajax({
    url: "/dqchecks_manvshive_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {

    for (c of cdr_types){
        var variance = c + "_variance";
        series_hive.push({
            name: variance,
            data: data[variance]
        });
    }
    // console.log(series_hive)

    var options = {
        series: series_hive,
        chart: {
            type: 'line',
            height: 350,
            width: '100%'
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            curve: 'smooth',
        },
        xaxis: {
            categories: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#000000',
                },
                formatter: function (x) {
                    if (x != null) {
                        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                    }
                    else {
                        return x
                    }
                }
            },
        },
        fill: {
            opacity: 1
        },
        grid: {
            borderColor: '#e7e7e7',
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
    };
    variance_chart = new ApexCharts(document.querySelector("#variances_hive_dashboard"), options);
    variance_chart.render();
});


$.ajax({
    url: "/dqchecks_manvsoracle_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {

    for (c of cdr_types){
        var variance = c + "_variance";
        series_oracle.push({
            name: variance,
            data: data[variance]
        });
    }
    // console.log(series_oracle)

    var options = {
        series: series_oracle,
        chart: {
            type: 'line',
            height: 350,
            width: '100%'
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            curve: 'smooth',
        },
        xaxis: {
            categories: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#000000',
                },
                formatter: function (x) {
                    if (x != null) {
                        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                    }
                    else {
                        return x
                    }
                }
            },
        },
        fill: {
            opacity: 1
        },
        grid: {
            borderColor: '#e7e7e7',
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
    };
    variance_chart = new ApexCharts(document.querySelector("#variances_oracle_dashboard"), options);
    variance_chart.render();
});

var today = new Date();
var time = today.getTime()

function diff_hour(t2,t1) {
    var diff = (t2-t1) / 1000;
    diff /= 3600;
    console.log(Math.abs(diff));
    return Math.abs(diff);
}

$(document).ready(function() {
    $('#pending_hdfs').DataTable({
        "createdRow": function (row, data, index) {
            if (parseInt(data[1]) >= 1000) {
                $('td', row).eq(1).css('color','red');
            }
            var string_time = data[2].substring(0, 4) + "-" + data[2].substring(4, 6) + "-" + data[2].substring(6, 8) + "T" + data[2].substring(8, 10) + ":" + data[2].substring(10, 12) + ":" + data[2].substring(12, 14);
            var row_time = new Date(string_time);
            var row_time = row_time.getTime();
            if (diff_hour(row_time, time) >= 1) {
                $('td', row).eq(2).css('color', 'red');
            }
        }
    });
    $('#pending_hive').DataTable({
        "createdRow": function (row, data, index) {
            if (data[1] >= 1000) {
                $('td', row).eq(1).css('color', 'red');
            }
            var string_time = data[2].substring(0, 4) + "-" + data[2].substring(4, 6) + "-" + data[2].substring(6, 8) + "T" + data[2].substring(8, 10) + ":" + data[2].substring(10, 12) + ":" + data[2].substring(12, 14);
            var row_time = new Date(string_time);
            var row_time = row_time.getTime();
            if (diff_hour(row_time, time) >= 1) {
                $('td', row).eq(2).css('color', 'red');
            }
        }
    });
});