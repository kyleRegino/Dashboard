var subsdump_oracle_chart;

function check_null(cdr_array) {
    var is_nulls = cdr_array.every((val, i, arr) => val === arr[0])
    if (is_nulls) {
        return new Array(cdr_array.length).fill(0)
    }
    else {
        return cdr_array
    }
}

$('#min_oracle').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_oracle').val() ? jQuery('#max_oracle').val() : false
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


$(document).ready(function () {
    $.ajax({
        url: "/dq_subsdump_oracle",
        method: "GET",
        dataType: "json"
    }).done(function (data) {
        count_lines = []
        for (d in data["data"]) {
            table_count = {
                name: d,
                data: data["data"][d],
                type: 'line'
            }
            count_lines.push(table_count)
        }
        var date_list = check_null(data["dates"])
        var options = {
            series: count_lines,
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
                categories: date_list,
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
        subsdump_oracle_chart = new ApexCharts(document.querySelector("#subsdump_oracle"), options);
        subsdump_oracle_chart.render();
    });
});


$("#oracle_subsdump_form").submit(function (e) {
    e.preventDefault();
    var start_date = $("#min_oracle").val();
    var end_date = $("#max_oracle").val();
    $.ajax({
        url: "/dq_subsdump_oracle",
        method: "POST",
        data: {
            "start_date": start_date,
            "end_date": end_date
        }
    }).done(function (data) {
        count_lines = []
        for (d in data["data"]) {
            table_count = {
                name: d,
                data: data["data"][d],
                type: 'line'
            }
            count_lines.push(table_count)
        }
        var date_list = check_null(data["dates"])
        subsdump_oracle_chart.updateOptions({
            xaxis: {
                categories: date_list,
            }
        });
        subsdump_oracle_chart.updateSeries(count_lines);
    });
});