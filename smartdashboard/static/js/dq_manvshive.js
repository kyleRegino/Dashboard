$.ajax({
    url: "/get_dqchecks_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    console.log(data);
    // COM
    var options_com = {
        series: [{
            name: 'Manifests',
            data: data["com_manifest"]
        }, {
            name: 'T1',
            data: data["com_t1"]
        }, {
            name: 'Variance',
            data: data["com_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };
    
    var chart_com = new ApexCharts(document.querySelector("#com_hive"), options_com);
    chart_com.render();

    // VOU
    var options_vou = {
        series: [{
            name: 'Manifests',
            data: data["vou_manifest"]
        }, {
            name: 'T1',
            data: data["vou_t1"]
        }, {
            name: 'Variance',
            data: data["vou_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };

    var chart_vou = new ApexCharts(document.querySelector("#vou_hive"), options_vou);
    chart_vou.render();

    // FIRST
    var options_first = {
        series: [{
            name: 'Manifests',
            data: data["first_manifest"]
        }, {
            name: 'T1',
            data: data["first_t1"]
        }, {
            name: 'Variance',
            data: data["first_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };

    var chart_first = new ApexCharts(document.querySelector("#first_hive"), options_first);
    chart_first.render();

    // MON
    var options_mon = {
        series: [{
            name: 'Manifests',
            data: data["mon_manifest"]
        }, {
            name: 'T1',
            data: data["mon_t1"]
        }, {
            name: 'Variance',
            data: data["mon_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };

    var chart_mon = new ApexCharts(document.querySelector("#mon_hive"), options_mon);
    chart_mon.render();

    // CM
    var options_cm = {
        series: [{
            name: 'Manifests',
            data: data["cm_manifest"]
        }, {
            name: 'T1',
            data: data["cm_t1"]
        }, {
            name: 'Variance',
            data: data["cm_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };

    var chart_cm = new ApexCharts(document.querySelector("#cm_hive"), options_cm);
    chart_cm.render();

    // ADJ
    var options_adj = {
        series: [{
            name: 'Manifests',
            data: data["adj_manifest"]
        }, {
            name: 'T1',
            data: data["adj_t1"]
        }, {
            name: 'Variance',
            data: data["ajd_variance"]
        }],
        chart: {
            type: 'bar',
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
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23],
        },
        fill: {
            opacity: 1
        },
    };

    var chart_adj = new ApexCharts(document.querySelector("#adj_hive"), options_adj);
    chart_adj.render();

});









