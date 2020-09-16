var cdr_types = ["com", "vou", "cm", "adj", "first", "mon", "data", "voice", "sms", "clr"];
var charts = [];
var lines = [];
var variance_chart = null;
var url = "/dqchecks_manvs"+page+"_js";

function check_null(cdr_array) {
    var is_nulls = cdr_array.every( (val,i,arr) => val === arr[0] )
    if (is_nulls) {
        return new Array(cdr_array.length).fill(0)
    }
    else {
        return cdr_array
    }
}

function update_data(cdr_date){
    $.ajax({
        url: url,
        method: "POST",
        dataType: "json",
        data: {"cdr_date": cdr_date}
    }).done(function (data) {
        lines = [];
        for (var i = 0; i < charts.length; i++) {
            var manifest_key = cdr_types[i] + "_manifest";
            var t1_key = cdr_types[i] + "_t1";
            var variance_key = cdr_types[i] + "_variance";
            var manifest = check_null(data[manifest_key]);
            var t1 = check_null(data[t1_key]);
            var variance = check_null(data[variance_key]);
            charts[i].updateSeries([{
                name: 'Manifests',
                data: manifest
            }, {
                name: 'T1',
                data: t1
            }, {
                name: 'Variance',
                data: variance
            }]);
            var overall_variance = check_null(data[variance_key]);
            lines.push({
                name: cdr_types[i] + ' variance',
                data: variance,
                type: 'line'
            });
        }
        variance_chart.updateSeries(lines);
    });
}


$.ajax({
    url: url,
    method: "GET",
    dataType: "json"
}).done(function (data) {
    for (c of cdr_types){
        var manifest_key = c + "_manifest";
        var t1_key = c + "_t1";
        var variance_key = c + "_variance";
        var manifest = check_null(data[manifest_key]);
        var t1 = check_null(data[t1_key]);
        var variance = check_null(data[variance_key]);
        var queryselect = "#"+ c + "_"+page;
        
        var options = {
            series: [{
                name: 'Manifests',
                data: manifest,
                type: 'column'
            }, {
                name: 'T1',
                data: t1,
                type: 'column'
            }, {
                name: 'Variance',
                data: variance,
                type: 'line'
            }],
            chart: {
                type: 'line',
                height: 350,
                toolbar: {
                    show: true,
                    offsetX: 0,
                    offsetY: 0,
                    tools: {
                        download: true,
                        selection: true,
                        zoom: true,
                        zoomin: true,
                        zoomout: true,
                        pan: true,
                        customIcons: []
                    },
                    export: {
                        csv: {
                            filename: "hallo",
                            columnDelimiter: ',',
                            headerCategory: 'category',
                            headerValue: 'value',
                            dateFormatter(timestamp) {
                                return new Date(timestamp).toDateString()
                            }
                        }
                    },
                    autoSelected: 'zoom'
                },
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                },
            },
            colors: ["#283593", "#F57C00", "#8BC34A"],
            dataLabels: {
                enabled: true,
                enabledOnSeries: [2],
                formatter: function (x) {
                    if (x != null) {
                        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                    }
                    else {
                        return ""
                    }
                }
            },
            stroke: {
                show: true,
                width: 2,
                curve: 'smooth'
                // colors: ['transparent']
            },
            grid: {
                borderColor: '#e7e7e7',
                row: {
                    colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
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
                            return ""
                        }
                    }
                },
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
            data: variance,
            type: 'line'
        });
    }
    var options = {
        series: lines,
        chart: {
            type: 'line',
            height: 350,
            toolbar: {
                export: {
                    csv: {
                        filename: "hallo",
                        columnDelimiter: ',',
                        headerCategory: 'hour',
                        headerValue: 'hour',
                    }
                },
            },
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
            curve: 'smooth'
        },
        grid: {
            borderColor: '#e7e7e7',
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
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
                        return ""
                    }
                }
            },
        },
        fill: {
            opacity: 1
        },
        markers: {
            size: 3
        },
    };
    variance_selector = "#variances_"+page
    variance_chart = new ApexCharts(document.querySelector(variance_selector), options);
    variance_chart.render();
});

// FOR CHANGING DATE AND UPDATING DATA
var form_selector = "#cdr_date_form_"+page;
var form_url = "/dqchecks_manvs"+page+"_search";
$(form_selector).submit(function (event) {
    event.preventDefault();
    var cdr_date = $("#cdr_date").val();
    $.ajax({
        url: form_url,
        method: "POST",
        data: { "date": cdr_date }
    }).done(function (data) {
        $("#variance_com").text(data.variance_com);
        $("#variance_cm").text(data.variance_cm);
        $("#variance_vou").text(data.variance_vou);
        $("#variance_adj").text(data.variance_adj);
        $("#variance_first").text(data.variance_first);
        $("#variance_mon").text(data.variance_mon);
        $("#variance_data").text(data.variance_data);
        $("#variance_voice").text(data.variance_voice);
        $("#variance_sms").text(data.variance_sms);
        $("#variance_clr").text(data.variance_clr);
        update_data(cdr_date);
        var today = new Date();
        var date_today = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        if (cdr_date != date_today) {
            update_colors();
        }
    });

});

// THRESHOLD
$("#form_threshold").submit(function (event) {
    event.preventDefault();
    var cdrs = $("#cdrs").val();
    var threshold = $("#threshold").val();
    $.ajax({
        url: "/dqchecks_update_threshold",
        method: "POST",
        data: { "cdrs": cdrs,
                "threshold": threshold}
    }).done(function (data) {
        $("#modal_threshold_hive").modal("hide");
    });

});