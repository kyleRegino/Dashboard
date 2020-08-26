var options = {
    series: [{
        name: 'Manifests',
        data: [21579,20771,36944,16279,16463,20933,36944,93038,113429,100320,82590,90566,95418,101506,105251,85105,96865,105343,117583,116228,83028,71661,43399,19413]
    }, {
        name: 'T1',
            data: [19831,19198,37162,18646,16377,19421,30477,55245,142334,105270,77920,92076,94395,101429,107562,84912,92051,106283,115463,120414,87473,67378,56132,23207]
    }, {
        name: 'Variance',
        data: [-1748,-1573,218,2367,-86,-1512,-6467,-37793,28905,4950,-4670,1510,-1023,-77,2311,-193,-4814,940,-2120,4186,4445,-4283,12733,3794]
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

var chart = new ApexCharts(document.querySelector("#com"), options);
chart.render();