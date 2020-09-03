var cdr_types = ["com", "vou", "cm", "adj", "first", "mon"];
var charts = [];
var lines = [];
var variance_chart = null;

var series = [];

console.log(lines)
console.log(charts)
$.ajax({
    url: "/dqchecks_manvshive_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {

    for (c of cdr_types){
        var variance = c + "_variance";
        series.push({
            name: variance,
            data: data[variance]
        });
    }
    console.log(series)

    var options = {
        series: series,
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