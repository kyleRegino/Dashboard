$.ajax({
    url: "/topsku_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    var options = {
        series: [{
        name: 'Home',
        type: 'column',
        data: data["home"]
      }, {
        name: 'Smart Bro Prepaid',
        type: 'column',
        data: data["smart_bro_prepaid"]
      }, {
        name: 'Smart Prepaid',
        type: 'column',
        data: data["smart_prepaid"]
      }, {
        name: 'Sun BW FLP',
        type: 'column',
        data: data["sun_bwl_flp"]
      }, {
        name: 'Sun BW Prepaid',
        type: 'column',
        data: data["sun_bwl_prepaid"]
      }, {
        name: 'Revenue',
        type: 'line',
        data: [20, 29, 37, 36, 44, 45]
      }],
        chart: {
          height: 350,
          type: 'line',
          stacked: false,
          // toolbar: {
          //     show: true,
          //     autoSelected: 'zoom'
          // }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '20%',
          endingShape: 'rounded'
        },
      },
      dataLabels: {
        enabled: false,
        // enabledOnSeries: [2]
      },
      stroke: {
        show: true,
        width: [0, 0, 0, 0, 0, 5]
      },
      title: {
        text: 'Amount per Brand every 4hrs',
        align: 'left',
        offsetX: 110
      },
      xaxis: {
        categories: ['0500H', '0900H', '1300H', '1700H', '2100H', '0100H'],
      },
      yaxis: [
        {
            seriesName: 'Home',
            // axisTicks: {
            //   show: true
            // },
            // axisBorder: {
            //   show: true,
            // },
            // labels: {
            //     style: {
            //       colors: '#008FFB',
            //     }
            // },
            // title: {
            //   text: "Columns"
            // },
            tooltip: {
                enabled: true
              }
          },
          {
            seriesName: 'Home',
            show: false,
            axisTicks: {
                show: true
              },
              axisBorder: {
                show: true,
              },
              labels: {
                  style: {
                    colors: '#008FFB',
                  }
              },
              title: {
                text: "Columns"
              },
              tooltip: {
                  enabled: true
                }
          }, 
          {
            seriesName: 'Home',
            show: false,
            axisTicks: {
                show: true
              },
              axisBorder: {
                show: true,
              },
              labels: {
                  style: {
                    colors: '#008FFB',
                  }
              },
              title: {
                text: "Columns"
              },
              tooltip: {
                  enabled: true
                }
          }, 
          {
            seriesName: 'Home',
            show: false,
            axisTicks: {
                show: true
              },
              axisBorder: {
                show: true,
              },
              labels: {
                  style: {
                    colors: '#008FFB',
                  }
              },
              title: {
                text: "Columns"
              },
              tooltip: {
                  enabled: true
                }
          }, 
          {
            seriesName: 'Home',
            show: false,
            axisTicks: {
                show: true
              },
              axisBorder: {
                show: true,
              },
              labels: {
                  style: {
                    colors: '#008FFB',
                  }
              },
              title: {
                text: "Columns"
              },
              tooltip: {
                  enabled: true
                }
          }, {
            opposite: true,
            seriesName: 'Revenue',
            axisTicks: {
              show: true
            },
            axisBorder: {
              show: true,
            },
            labels: {
                style: {
                  colors: '#FEB019',
                },
            },
            title: {
              text: "Line"
            }
          }
      ],
      tooltip: {
        fixed: {
          enabled: true,
          position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
          offsetY: 30,
          offsetX: 60
        },
      },
      legend: {
        horizontalAlign: 'left',
        offsetX: 40
      },
    };


    var chart = new ApexCharts(document.querySelector("#topsku"), options);
    chart.render();
});