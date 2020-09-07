var cdr_types = ["home", "smart bro prepaid", "smart prepaid", "sun bw flp", "sun bw prepaid", "sun flp", "sun prepaid", "tnt"]; //
var series_hour = [];
var series_day = [];

$.ajax({
    url: "/topsku_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {

  // PER HOUR
  for (c of cdr_types){
    var brand = c;
    series_hour.push({
        name: brand,
        data: data[brand],
        type: 'bar'
    });
  }
  series_hour.push({
    name: 'Total per Hour',
    data: data['total_hour'],
    type: 'line'

  })
  console.log(series_hour)

  var options_hour = {
    series: series_hour,
    chart: {
      height: 350,
      type: 'line',
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '10%',
        endingShape: 'rounded'
      },
    },
    colors: ['#77B6EA', '#545454', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E"],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: [0, 0, 0, 0, 0, 5],
      curve: 'smooth'
    },
    grid: {
      borderColor: '#e7e7e7',
      row: {
        colors: ['#f3f3f3', 'transparent'], 
        opacity: 0.5
      },
    },
    fill: {
      opacity: 1
    },
    // title: {
    //   text: 'Amount per Brand every 4hrs',
    //   align: 'left',
    //   offsetX: 110
    // },
    xaxis: {
      categories: ['0500H', '0900H', '1300H', '1700H', '2100H', '0100H'],
    },
  };
  var chart = new ApexCharts(document.querySelector("#topsku"), options_hour);
  chart.render();

  // PER DAY
  // var options_day = {
  //   series: [{
  //     name: 'Total Amount per Day',
  //     data: data['total_day'],
  //     type: 'bar'
  //   }],
  //   chart: {
  //     height: 350,
  //     type: 'line',
  //   },
  //   plotOptions: {
  //     bar: {
  //       // horizontal: false,
  //       columnWidth: '5%',
  //       endingShape: 'rounded'
  //     },
  //   },
  //   dataLabels: {
  //     enabled: false,
  //   },
  //   stroke: {
  //     show: true,
  //     width: 2,
  //     curve: 'smooth'
  //   },
  //   grid: {
  //     borderColor: '#e7e7e7',
  //     row: {
  //       colors: ['#f3f3f3', 'transparent'], 
  //       opacity: 0.5
  //     },
  //   },
  //   fill: {
  //     opacity: 1
  //   },
  //   title: {
  //     text: 'Amount of Brands Weekly',
  //     align: 'left',
  //     offsetX: 110
  //   },
  //   xaxis: {
  //     categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
  //   },
  // };
  // var day = new ApexCharts(document.querySelector("#topsku_day"), options_day);
  // day.render();
  
  
});



