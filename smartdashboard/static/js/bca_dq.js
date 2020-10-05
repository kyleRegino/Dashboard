// PRP ACCT INIT VAR
var prp_acct_chart;
var prp_bal = []
var prp_count = []
var prp_su = []
// PCODES INIT VAR
var pcodes_total_topup = []
var pcodes_topup_count = []
var pcodes_total_count = []
var pcodes_chart;

function check_null(cdr_array) {
    var is_nulls = cdr_array.every((val, i, arr) => val === arr[0])
    if (is_nulls) {
        return new Array(cdr_array.length).fill(0)
    }
    else {
        return cdr_array
    }
}

$('#min_prp').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_prp').val() ? jQuery('#max_prp').val() : false
        })
    }
});

$('#max_prp').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_prp').val() ? jQuery('#min_prp').val() : false
        })
    }
});

$('#min_pcodes').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_pcodes').val() ? jQuery('#max_pcodes').val() : false
        })
    }
});

$('#max_pcodes').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_pcodes').val() ? jQuery('#min_pcodes').val() : false
        })
    }
});

$(document).ready(function () {
    init_prp();
    init_pcodes();
});

function init_prp() {
    $.ajax({
        url: "/bca_monitoring_dq_prp",
        method: "GET",
    }).done(function (data) {
        prp_bal = []
        prp_count = []
        prp_su = []
        for (d in data["data"]) {
            lines_bal = {
                name: d,
                data: data["data"][d]["bal"],
                type: 'line'
            }
            lines_count = {
                name: d,
                data: data["data"][d]["count"],
                type: 'line'
            }
            lines_su = {
                name: d,
                data: data["data"][d]["su"],
                type: 'line'
            }
            prp_bal.push(lines_bal)
            prp_count.push(lines_count)
            prp_su.push(lines_su)
        }
        var options = {
            series: prp_bal,
            chart: {
                type: 'line',
                height: 350,
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                },
            },
            colors: ['#77B6EA', '#545454', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E"],
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
                    formatter: function (x) {
                        if (x != null) {
                            return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                        }
                        else {
                            return ""
                        }
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

        prp_acct_chart = new ApexCharts(document.querySelector("#prp_acct_chart"), options);
        prp_acct_chart.render();
    });
}

function init_pcodes() {
    $.ajax({
        url: "/bca_monitoring_dq_pcodes",
        method: "GET",
    }).done(function (data) {
        pcodes_total_topup = []
        pcodes_topup_count = []
        pcodes_total_count = []
        for (d in data["data"]) {
            lines_total_topup = {
                name: d,
                data: data["data"][d]["total_topup"],
                type: 'line'
            }
            lines_topup_count = {
                name: d,
                data: data["data"][d]["topup_count"],
                type: 'line'
            }
            lines_total_count = {
                name: d,
                data: data["data"][d]["total_count"],
                type: 'line'
            }
            pcodes_total_topup.push(lines_total_topup)
            pcodes_topup_count.push(lines_topup_count)
            pcodes_total_count.push(lines_total_count)
        }
        var options = {
            series: pcodes_total_topup,
            chart: {
                type: 'line',
                height: 350,
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                },
            },
            colors: ['#77B6EA', '#545454', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E"],
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
                    formatter: function (x) {
                        if (x != null) {
                            return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                        }
                        else {
                            return ""
                        }
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

        pcodes_chart = new ApexCharts(document.querySelector("#pcodes_chart"), options);
        pcodes_chart.render();
    });
}

$("#prp_attr").change(function() {
    var attr = $("#prp_attr").val();
    if (attr == "total_bal") {
        prp_acct_chart.updateSeries(prp_bal)
    }
    else if (attr == "total_count") {
        prp_acct_chart.updateSeries(prp_count)
    }
    else if (attr == "total_su") {
        prp_acct_chart.updateSeries(prp_su)
    }
});

$("#pcodes_attr").change(function () {
    var attr = $("#pcodes_attr").val();
    if (attr == "total_topup") {
        pcodes_chart.updateSeries(pcodes_total_topup)
    }
    else if (attr == "topup_count") {
        pcodes_chart.updateSeries(pcodes_topup_count)
    }
    else if (attr == "total_count") {
        pcodes_chart.updateSeries(pcodes_total_count)
    }
});

$("#prp_acct_form").submit(function (e) {
    e.preventDefault();
    var start_date = $("#min_prp").val();
    var end_date = $("#max_prp").val();
    $.ajax({
        url: "/bca_monitoring_dq_prp",
        method: "POST",
        data: {
            "start_date": start_date,
            "end_date": end_date
        }
    }).done(function (data) {
        prp_bal = []
        prp_count = []
        prp_su = []
        for (d in data["data"]) {
            bal = check_null(data["data"][d]["bal"])
            count = check_null(data["data"][d]["count"])
            su = check_null(data["data"][d]["su"])
            lines_bal = {
                name: d,
                data: bal,
                type: 'line'
            }
            lines_count = {
                name: d,
                data: count,
                type: 'line'
            }
            lines_su = {
                name: d,
                data: su,
                type: 'line'
            }
            prp_bal.push(lines_bal)
            prp_count.push(lines_count)
            prp_su.push(lines_su)
        }
        dates = check_null(data["dates"])
        prp_acct_chart.updateOptions({
            xaxis: {
                categories: dates,
            }
        });
        var attr = $("#prp_attr").val();
        if (attr == "total_bal") {
            prp_acct_chart.updateSeries(prp_bal)
        }
        else if (attr == "total_count") {
            prp_acct_chart.updateSeries(prp_count)
        }
        else if (attr == "total_su") {
            prp_acct_chart.updateSeries(prp_su)
        }
    });
});

$("#pcodes_form").submit(function (e) {
    e.preventDefault();
    var start_date = $("#min_pcodes").val();
    var end_date = $("#max_pcodes").val();
    $.ajax({
        url: "/bca_monitoring_dq_pcodes",
        method: "POST",
        data: {
            "start_date": start_date,
            "end_date": end_date
        }
    }).done(function (data) {
        pcodes_total_topup = []
        pcodes_topup_count = []
        pcodes_total_count = []
        for (d in data["data"]) {
            total_topup = check_null(data["data"][d]["total_topup"]);
            topup_count = check_null(data["data"][d]["topup_count"]);
            total_count = check_null(data["data"][d]["total_count"]);
            lines_total_topup = {
                name: d,
                data: total_topup,
                type: 'line'
            }
            lines_topup_count = {
                name: d,
                data: topup_count,
                type: 'line'
            }
            lines_total_count = {
                name: d,
                data: total_count,
                type: 'line'
            }
            pcodes_total_topup.push(lines_total_topup)
            pcodes_topup_count.push(lines_topup_count)
            pcodes_total_count.push(lines_total_count)
        }
        dates = check_null(data["dates"])
        pcodes_chart.updateOptions({
            xaxis: {
                categories: dates,
            }
        });
        var attr = $("#pcodes_attr").val();
        if (attr == "total_topup") {
            pcodes_chart.updateSeries(pcodes_total_topup)
        }
        else if (attr == "topup_count") {
            pcodes_chart.updateSeries(pcodes_topup_count)
        }
        else if (attr == "total_count") {
            pcodes_chart.updateSeries(pcodes_total_count)
        }
    });
});