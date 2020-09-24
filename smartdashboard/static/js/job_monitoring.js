$.ajax({
    url: "/get_job_monitoring",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    // console.log(data.job_status[0]);
    // console.log(data.job_Label[0]);
    var options = {
        series: [ data.job_status[0], data.job_status[1], data.job_status[2], data.job_status[3]],
        labels: [data.job_Label[0], data.job_Label[1], data.job_Label[2], data.job_Label[3]],
        plotOptions: {
            pie: {
              donut: {
                size: '65%',
                background: 'transparent',
                labels: {
                  show: true,
                  name: {
                    show: true,
                    fontSize: '22px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 600,
                    color: undefined,
                    offsetY: -10,
                    formatter: function (val) {
                      return val
                      // .toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
                    }
                  },
                  value: {
                    show: true,
                    fontSize: '16px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 400,
                    color: undefined,
                    offsetY: 16,
                    formatter: function (val) {
                      return val
                      // .toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
                    }
                  },
                  total: {
                    show: true,
                    showAlways: false,
                    label: 'Total',
                    fontSize: '22px',
                    fontFamily: 'Helvetica, Arial, sans-serif',
                    fontWeight: 600,
                    color: '#373d3f',
                    formatter: function (w) {
                      w.globals.seriesTotals.reduce((a, b) => {
                        return a + b
                      }, 0)
                      // .toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
                    }
                  }
                }
              },   
            }
        },
        

        chart: {
            width: "100%",
            type: 'donut', 
        },
        colors: ['#ffaf00', '#19d895', "#ff6258", "#8862e0"],
        dataLabels: {
            enabled: true,
        },
        title: {
            text: 'Overall Status',
            align: 'left',
            // margin: 10,
            offsetX: 0,
            offsetY: 0,
            floating: false,
            style: {
              fontSize:  '30px',
              fontWeight:  'bold',
              fontFamily: undefined,
              color:  '#263238'
            },
        },
        tooltip: {
          enabled: true,
          y: {
            formatter: function(val) {
              return val
              // .toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
            },
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          }
        },      
        legend: {
          position: 'bottom',
          horizontalAlign: 'center',
        },    
    };
    
    var chart = new ApexCharts(document.querySelector("#donutchart"), options, options.plotOptions);
    chart.render();
});

$.ajax({
  url: "/lrj_js",
  method: "GET",
  dataType: "json"
}).done(function (data) {
  // console.log(data.job_status[0]);
  // console.log(data.job_Label[0]);
  var options = {
      series: [ data.job_status[0], data.job_status[1], data.job_status[2], data.job_status[3]],
      labels: [data.job_Label[0], data.job_Label[1], data.job_Label[2], data.job_Label[3]],
      chart: {
        width: "100%",
        type: 'donut',
      },
      plotOptions: {
          pie: {
            donut: {
              size: '65%',
              background: 'transparent',
              labels: {
                show: true,
                name: {
                  show: true,
                  fontSize: '22px',
                  fontFamily: 'Helvetica, Arial, sans-serif',
                  fontWeight: 600,
                  color: undefined,
                  offsetY: -10,
                  formatter: function (val) {
                    return val.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
                  }
                },
                value: {
                  show: true,
                  fontSize: '16px',
                  fontFamily: 'Helvetica, Arial, sans-serif',
                  fontWeight: 400,
                  color: undefined,
                  offsetY: 16,
                  formatter: function (val) {
                    return val.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
                  }
                },
                total: {
                  show: true,
                  showAlways: false,
                  label: 'Total',
                  fontSize: '150%',
                  fontFamily: 'Helvetica, Arial, sans-serif',
                  fontWeight: 600,
                  color: '#373d3f',
                  formatter: function (w) {
                    total =  w.globals.seriesTotals.reduce((a, b) => {
                      return a + b
                    }, 0)
                    // .toFixed(2).replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                  }
                }
              }
            },   
          }
      },
      
      colors: ['#ffaf00', '#19d895', "#ff6258", "#8862e0"],
      dataLabels: {
          enabled: true,
      },    
      tooltip: {
        enabled: true,
        y: {
          formatter: function(val) {
            return val.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
          },
          title: {
            formatter: function (seriesName) {
              return ''
            }
          }
        }
      }, 
      legend: {
        position: 'bottom',
        horizontalAlign: 'center',
      },
  };
  


  var chart = new ApexCharts(document.querySelector("#donutchart_longrunning"), options);
  chart.render();
});

$.ajax({
  url: "/lrj_js",
  method: "GET",
  dataType: "json"
}).done(function (data) {
  var options = {
    series: [ { data: [data.job_status[0], data.job_status[1], data.job_status[2], data.job_status[3]] } ],
    chart: {
      height: 200,
      width: "100%",
      type: 'bar',
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '70%'
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
    fill: {
      opacity: 1
    },
    xaxis: {
      categories: [data.job_Label[0], data.job_Label[1], data.job_Label[2], data.job_Label[3]],
    },
  };



  var chart = new ApexCharts(document.querySelector("#barchart_longrunning"), options);
  chart.render();
});







