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
                      return w.globals.seriesTotals.reduce((a, b) => {
                        return a + b
                      }, 0)
                    }
                  }
                }
              },   
            }
        },
        

        chart: {
            width: 500,
            type: 'donut', 
        },
        colors: ['#ffaf00', '#19d895', "#ff6258", "#8862e0"],
        dataLabels: {
            enabled: true,
            // formatter: function (val) {
            //     return val + "%"
            // }
        },
        // responsive: [{
        //     breakpoint: 480,
        //     options: {
        //         chart: {
        //         width: 500
        //         },
        //         legend: {
        //             show: false
        //         },
        //     }
        // }],
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
        legend: {
          position: 'bottom',
          horizontalAlign: 'center',
          // offsetY: 0,
          // height: 230,
        },
        // legend: {
        //     position: 'top',
        //     horizontalAlign: 'right',
        //     floating: true,
        //     offsetY: -25,
        //     offsetX: 20
        // },
        
        
        
    };
    


    var chart = new ApexCharts(document.querySelector("#donutchart"), options, options.plotOptions);
    chart.render();
});

$.ajax({
  url: "/get_long_running_jobs",
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
                    return w.globals.seriesTotals.reduce((a, b) => {
                      return a + b
                    }, 0)
                  }
                }
              }
            },   
          }
      },
      

      chart: {
          width: 500,
          type: 'donut', 
      },
      colors: ['#ffaf00', '#19d895', "#ff6258", "#8862e0"],
      dataLabels: {
          enabled: true,
          // formatter: function (val) {
          //     return val + "%"
          // }
      },
      // responsive: [{
      //     breakpoint: 480,
      //     options: {
      //         chart: {
      //         width: 500
      //         },
      //         legend: {
      //             show: false
      //         },
      //     }
      // }],
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
      legend: {
        position: 'bottom',
        horizontalAlign: 'center',
        // offsetY: 0,
        // height: 230,
      },
      // legend: {
      //     position: 'top',
      //     horizontalAlign: 'right',
      //     floating: true,
      //     offsetY: -25,
      //     offsetX: 20
      // },
      
      
      
  };
  


  var chart = new ApexCharts(document.querySelector("#donutchart_longrunning"), options, options.plotOptions);
  chart.render();
});







