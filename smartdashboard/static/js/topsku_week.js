var chart_week = null;
var series_week = [];
var weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];

$('#sku_min').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#sku_max').val() ? jQuery('#sku_max').val() : false
        })
    }
});

$('#sku_max').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#sku_min').val() ? jQuery('#sku_min').val() : false
        })
    }
});

$('#sku_table_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
});

$("#sku_week_form").submit(function (event) {
    event.preventDefault();
    var start_date = $("#sku_min").val();
    var end_date = $("#sku_max").val();
    update_week_sku(start_date,end_date);
});

$('#min_weekly_table').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_weekly_table').val() ? jQuery('#max_weekly_table').val() : false
        })
    },
    maxDateTime:true
});

$('#max_weekly_table').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_weekly_table').val() ? jQuery('#min_weekly_table').val() : false
        })
    },
    maxDateTime:true,
});

function update_week_sku(start_date, end_date) {
    $.ajax({
        url: "/topsku_week_js",
        method: "POST",
        dataType: "json",
        data: { "start_date": start_date,
                "end_date": end_date
            }
    }).done(function (data) {
        updated_series = [{
            name: "Amounts",
            data: data["amounts"],
            type: 'bar'
            },
            {
                name: "Counts",
                data: data["counts"],
                type: 'line'
            }
        ]
        chart_week.updateOptions({
            xaxis: {
                categories: data["dates"],
            }
        }
        );
        chart_week.updateSeries(updated_series);
    });
}

$.ajax({
    url: "/topsku_week_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    var options = {
        series: [
            {
            name: "Amounts",
            data: data["amounts"],
            type: 'bar'
            },
            {
                name: "Counts",
                data: data["counts"],
                type: 'line'
            }
        ],
        chart: {
            height: 350,
            type: 'line',
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '55%',
                endingShape: 'rounded'
            },
        },
        colors: ['#008FFB', '#FEB019', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E"],
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 5,
            curve: 'smooth'
        },
        grid: {
            borderColor: '#e7e7e7',
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        fill: {
            opacity: 1
        },
        markers: {
            size: 2
        },
        xaxis: {
            categories: data["dates"],
        },
        yaxis: [
            {
                axisTicks: {
                    show: true,
                },
                axisBorder: {
                    show: true,
                    color: '#000000'
                },
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
                title: {
                    text: "Transaction Amounts",
                    style: {
                        color: '#000000',
                        fontSize: '0.8em',
                        fontWeight: 550,
                    }
                },
                tooltip: {
                    enabled: true
                }
            },
            {
                seriesName: 'Counts',
                opposite: true,
                axisTicks: {
                    show: true,
                },
                axisBorder: {
                    show: true,
                    color: '#000000'
                },
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
                title: {
                    text: "Transaction Counts",
                    style: {
                        color: '#000000',
                        fontSize: '0.8em',
                        fontWeight: 550,
                    }
                }
            }
        ]
    };

    chart_week = new ApexCharts(document.querySelector("#topsku_week"), options);
    chart_week.render();

});

function generate_sku_table(data) {
    var columns = [];
    columnNames = data.columns;
    for (var i in columnNames) {
        if (i == 0) {
            renderer = function (x) {
                return x
            }
        }
        else {
            renderer = $.fn.dataTable.render.number(',', '.', 2);
        }
        columns.push({
            data: columnNames[i],
            title: columnNames[i],
            render: renderer,
            className: columnNames[i]
        });
    }
    $('#topsku_table').DataTable({
        data: data.data,
        columns: columns
    });
};

function getData(cb_func,sku_date,hour) {
    $.ajax({
        url: "/topsku_week_table_js",
        type: "POST",
        data: {
            "sku_date": sku_date,
            "hour": hour
        },
        success: cb_func
    });
}

$(document).ready(function () {
    hour = get_current_hour()
    var today = new Date();
    if (hour == 1) {
        today.setDate(today.getDate() - 1);
    }
    var date = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    var day = weekday[today.getDay()];
    $("#sku_table_date").val(date);
    $("#sku_table_hour").val(hour);
    var text = "Topup Statistics as of " + date + ", " + day + ", Hour: " + hour + ":00"
    $("#current_time_status").text(text)
    getData(generate_sku_table, date, hour)
});

function update_table_week(sku_date, hour) {
    $('#topsku_table').DataTable().clear().destroy();
    $('#topsku_table').empty();
    getData(generate_sku_table, sku_date, hour)
}

$("#sku_table_form").submit(function (event) {
    event.preventDefault();
    var date = $("#sku_table_date").val();
    var hour = $("#sku_table_hour").val();
    var date_converted = new Date(date);
    var day = weekday[date_converted.getDay()];
    var text = "Topup Statistics as of " + date + ", " + day + ", Hour: " + hour + ":00"
    $("#current_time_status").text(text)
    update_table_week(date, hour);
});

function get_current_hour() {
    var date = new Date;
    var hour = date.getHours();
    if (hour > 1 && hour < 9) {
        return 5
    }
    else if (hour > 5 && hour < 13) {
        return 9
    }
    else if (hour > 9 && hour < 17) {
        return 13
    }
    else if (hour > 13 && hour < 21) {
        return 17
    }
    else if (hour > 17 && hour <= 24) {
        return 21
    }
    else if (hour < 5) {
        return 1
    }
}
