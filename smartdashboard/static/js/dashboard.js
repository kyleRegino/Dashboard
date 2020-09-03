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
    console.log(series_hive)

    var options = {
        series: series_hive,
        chart: {
            type: 'line',
            height: '200%',
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
    console.log(series_oracle)

    var options = {
        series: series_oracle,
        chart: {
            type: 'line',
            height: '200%',
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