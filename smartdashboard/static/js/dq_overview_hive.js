var cdr_types = ["com", "vou", "cm", "adj", "first", "mon", "data", "voice", "sms", "clr"];
var lines_hive = [];
var hive_variance_chart = null;
var submit_clicked = null;

function check_null(cdr_array) {
    var is_nulls = cdr_array.every((val, i, arr) => val === arr[0])
    if (is_nulls) {
        return new Array(cdr_array.length).fill(0)
    }
    else {
        return cdr_array
    }
}

$('#min_hive').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_hive').val() ? jQuery('#max_hive').val() : false
        })
    }
});

$('#max_hive').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_hive').val() ? jQuery('#min_hive').val() : false
        })
    }
});

$('#min_hive_table').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            maxDate: jQuery('#max_hive_table').val() ? jQuery('#max_hive_table').val() : false
        })
    }
});

$('#max_hive_table').datetimepicker({
    timepicker: false,
    format: 'Y-m-d',
    onShow: function (ct) {
        this.setOptions({
            minDate: jQuery('#min_hive_table').val() ? jQuery('#min_hive_table').val() : false
        })
    }
});

$("#search_date_hive").click(function(){
    if ($("#search_date_hive")[0].checkValidity()) {
        var start_date = $("#min_hive").val();
        var end_date = $("#max_hive").val();
        var period = $("#period_hive").val();
        if (start_date!= "" && end_date != "" && period != "") {
            update_data_hive(start_date, end_date, period);
        }
        else{
            alert("Form is not completed.")
        }
    }
    else {
        $("#search_date_hive")[0].reportValidity();
    }
});

function push_lines_hive(cdr, data_cdr) {
    lines_hive.push({
        name: cdr + ' variance',
        data: data_cdr,
        type: 'line'
    });
}

function update_data_hive(start_date,end_date,period) {
    $.ajax({
        url: "/dqchecks_overview_hive_js",
        method: "POST",
        dataType: "json",
        data: { "start_date": start_date,
                "end_date": end_date,
                "period": period }
    }).done(function (data) {
        lines_hive = [];
        for (c of cdr_types) {
            var variance = "variance_" + c;
            var data_cdr = check_null(data[variance]);
            push_lines_hive(c, data_cdr);
        }
        var date_list = check_null(data["date_list"])
        hive_variance_chart.updateOptions({
            xaxis: {
                categories: date_list,
            }
        }
        );
        hive_variance_chart.updateSeries(lines_hive);
    });
}

$.ajax({
    url: "/dqchecks_overview_hive_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    for (c of cdr_types) {
        var variance = "variance_" + c;
        var data_cdr = check_null(data[variance]);
        push_lines_hive(c, data_cdr);
    }
    var date_list = check_null(data["date_list"])
    var options = {
        series: lines_hive,
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
    hive_variance_chart = new ApexCharts(document.querySelector("#variances_hive"), options);
    hive_variance_chart.render();
});


$("#variance_table_form_hive").submit(function(event) {
    event.preventDefault();
    var start_date = $("#min_hive_table").val();
    var end_date = $("#max_hive_table").val();
    $('#hive_table').DataTable().clear().destroy();
    generate_table_hive(start_date, end_date);
});

function generate_table_hive(start_date,end_date) {
    $('#hive_table').DataTable({
        ajax: {
            url:'/dqchecks_hive_table',
            type: 'POST',
            dataType: "json",
            data: {
                "start_date": start_date,
                "end_date": end_date
            },
            dataSrc: 'data',
        },
        columns: [
            { data: 'file date' },
            { data: 'cdr' },
            { data: 'manifest count', className: 'dt-body-right' },
            { data: 't1 count', className: 'dt-body-right' },
            { data: 'variance', className: 'dt-body-right' }
        ],
        initComplete: function () {
            var column = this.api().column(1);
            var select = $("#cdr_select_hive").on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex(
                    $(this).val()
                );

                column
                    .search(val ? '^' + val + '$' : '', true, false)
                    .draw();
            });
            select.empty()
            select.append('<option value=""> ALL </option>')
            column.data().unique().sort().each(function (d, j) {
                select.append('<option value="' + d + '">' + d + '</option>')
            });
        }
    });
};
generate_table_hive(null, null);