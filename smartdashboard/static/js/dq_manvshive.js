var cdr_types = ["com", "vou", "cm", "adj", "first", "mon"];
var charts = [];
var lines = [];
var variance_chart = null;
function update_data_hive(cdr_date){
    $.ajax({
        url: "/dqchecks_manvshive_js",
        method: "POST",
        dataType: "json",
        data: {"cdr_date": cdr_date}
    }).done(function (data) {
        lines = [];
        for (var i = 0; i < charts.length; i++) {
            var manifest = cdr_types[i] + "_manifest";
            var t1 = cdr_types[i] + "_t1";
            var variance = cdr_types[i] + "_variance";
            charts[i].updateSeries([{
                name: 'Manifests',
                data: data[manifest]
            }, {
                name: 'T1',
                data: data[t1]
            }, {
                name: 'Variance',
                data: data[variance]
            }]);
            lines.push({
                name: cdr_types[i] + ' variance',
                data: data[variance],
                type: 'line'
            });
        }
        variance_chart.updateSeries(lines);
    });
}


$.ajax({
    url: "/dqchecks_manvshive_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    for (c of cdr_types){
        var manifest = c+"_manifest";
        var t1 = c + "_t1";
        var variance = c + "_variance";
        var queryselect = "#"+ c + "_hive";
        var options = {
            series: [{
                name: 'Manifests',
                data: data[manifest],
                type: 'column'
            }, {
                name: 'T1',
                data: data[t1],
                type: 'column'
            }, {
                name: 'Variance',
                data: data[variance],
                type: 'line'
            }],
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
            dataLabels: {
                enabled: true,
                enabledOnSeries: [2]
            },
            stroke: {
                show: true,
                width: 2,
                // colors: ['transparent']
            },
            xaxis: {
                categories: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            },
            fill: {
                opacity: 1
            },
        };
        var chart = new ApexCharts(document.querySelector(queryselect), options);
        charts.push(chart);
        chart.render();
        lines.push({
            name: c + ' variance',
            data: data[variance],
            type: 'line'
        });
    }
    var options = {
        series: lines,
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
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 2,
            // colors: ['transparent']
        },
        xaxis: {
            categories: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        },
        fill: {
            opacity: 1
        },
    };
    variance_chart = new ApexCharts(document.querySelector("#variances_hive"), options);
    variance_chart.render();
});







