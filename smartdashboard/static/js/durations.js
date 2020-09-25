var duration_graph;
var count_graph;
var sprint = page;
var sprint_url = "/" + sprint + "_api"
var form = "#" + sprint +"_duration_form"
var query_durations = "#" + sprint + "_durations"
var query_counts = "#" + sprint + "_counts"

function check_null(cdr_array) {
    var is_nulls = cdr_array.every((val, i, arr) => val === arr[0])
    if (is_nulls) {
        return new Array(cdr_array.length).fill(0)
    }
    else {
        return cdr_array
    }
}

$('#min_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_date').val() ? jQuery('#max_date').val() : false
        })
    }
});

$('#max_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_date').val() ? jQuery('#min_date').val() : false
        })
    }
});

$(form).submit(function(e){
    e.preventDefault();
    var start_date = $("#min_date").val();
    var end_date = $("#max_date").val();
    $.ajax({
        url: sprint_url,
        method: "POST",
        data: {
            "start_date": start_date,
            "end_date": end_date
        }
    }).done(function (data) {
        var lines_durations = []
        var lines_counts = []
        for (d in data["data"]) {
            duration = check_null(data["data"][d]["duration"])
            count = check_null(data["data"][d]["count"])
            lines_duration = {
                name: d,
                data: duration,
                type: 'line'
            }
            lines_count = {
                name: d,
                data: count,
                type: 'line'
            }
            lines_durations.push(lines_duration)
            lines_counts.push(lines_count)
        }
        dates = check_null(data["dates"])
        duration_graph.updateOptions({
            xaxis: {
                categories: dates,
            }
        });
        count_graph.updateOptions({
            xaxis: {
                categories: data["dates"],
            }
        });
        duration_graph.updateSeries(lines_durations)
        count_graph.updateSeries(lines_counts)
    });
});

$(document).ready(function(){
    $.ajax({
        url: sprint_url,
        method: "GET",
    }).done(function (data) {
        var lines_durations = []
        var lines_counts = []
        for (d in data["data"]){
            lines_duration = {
                name: d,
                data: data["data"][d]["duration"],
                type: 'line'
            }
            lines_count = {
                name: d,
                data: data["data"][d]["count"],
                type: 'line'
            }
            lines_durations.push(lines_duration)
            lines_counts.push(lines_count)
        }
        var options_durations = {
            series: lines_durations,
            chart: {
                type: 'line',
                height: 350,
            },
            title: {
                text: 'Average Duration',
                align: 'left',
                offsetX: 0,
                offsetY: 0,
                floating: false,
                style: {
                    fontSize: '20px',
                    fontFamily: undefined,
                    color: '#263238'
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
                categories: data["dates"]
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return new Date(value * 1000).toISOString().substr(11, 8);
                    }
                }
            },
            fill: {
                opacity: 1
            },
            markers: {
                size: 3
            },
        };

        var options_count = {
            series: lines_counts,
            chart: {
                type: 'line',
                height: 350
            },
            title: {
                text: 'File Counts',
                align: 'left',
                offsetX: 0,
                offsetY: 0,
                floating: false,
                style: {
                    fontSize: '20px',
                    fontFamily: undefined,
                    color: '#263238'
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
                curve: 'smooth',
            },
            xaxis: {
                categories: data["dates"],
            },
            fill: {
                opacity: 1
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
            markers: {
                size: 3
            },
        };
        duration_graph = new ApexCharts(document.querySelector(query_durations), options_durations);
        duration_graph.render();
        count_graph = new ApexCharts(document.querySelector(query_counts), options_count);
        count_graph.render();
    });
});