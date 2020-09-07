var chart_week = null;
var series_week = [];

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

$("#sku_week_form").submit(function (event) {
    event.preventDefault();
    var start_date = $("#sku_min").val();
    var end_date = $("#sku_max").val();
    update_week_sku(start_date,end_date);
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
                    color: '#008FFB'
                },
                labels: {
                    style: {
                        colors: '#008FFB',
                    }
                },
                title: {
                    text: "Transaction Amounts",
                    style: {
                        color: '#008FFB',
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
                    color: '#FEB019'
                },
                labels: {
                    style: {
                        colors: '#FEB019',
                    },
                },
                title: {
                    text: "Transaction Counts",
                    style: {
                        color: '#FEB019',
                    }
                }
            }
        ]
    };

    chart_week = new ApexCharts(document.querySelector("#topsku_week"), options);
    chart_week.render();

});