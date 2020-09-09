var series_amount = []
var series_count = [];
var y_axis_amount = [];
var color_pallete = ['#5b9bd5', '#ed7d31', '#ffd966', '#2b2d4f', '#00b050', '#bf9000', '#d6dce5', '#ffff00', '#99ff66', '#ffa500'];
var colors = [];
var chart_day;
var max_brand = 0;
var init_brand = 0;

$('#sku_date').datetimepicker({
  timepicker: false,
  format: 'Y-m-d',
});

$("#sku_day_form").submit(function(event){
  event.preventDefault();
  var sku_date = $("#sku_date").val();
  update_day_sku(sku_date);
});

function series_amount_push(brand, brand_amount) {
  series_amount.push({
    name: brand,
    data: brand_amount,
    type: 'bar'
  });
}

function series_count_push(brand, brand_count) {
  series_count.push({
    name: brand,
    data: brand_count,
    type: 'bar'
  });
}

function compute_max_brand(brand_max, brand) {
  if (init_brand < brand_max) {
    init_brand = brand_max
    max_brand = brand
  }
}

function create_yaxis() {
  for (var i = 0; i < series_amount.length; i++) {
    if (i == 0) {
      show_y = true
    }
    else {
      show_y = false
    }
    y_axis_amount.push({
      seriesName: max_brand,
      show: show_y,
      opposite: false,
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
          return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
      },
      title: {
        text: "Total Amounts Per Brand Over Hour",
        style: {
          color: '#000000',
          fontSize: '0.8em',
        }
      }
    })
  }
}

function push_totals(total_amt, total_cnt) {
  series_amount.push({
    name: "Total Amounts Per Hour",
    data: total_amt,
    type: 'line'
  });
  series_count.push({
    name: "Total Counts Per Hour",
    data: total_cnt,
    type: 'line'
  });

  y_axis_amount.push({
    seriesName: "Total Amounts Per Hour",
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
        return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
      }
    },
    title: {
      text: "Total Amounts Over Hour",
      style: {
        color: '#000000',
        fontSize: '0.8em',
      }
    }
  });
}

function update_day_sku(sku_date) {
  $.ajax({
    url: "/topsku_day_js",
    method: "POST",
    dataType: "json",
    data: { "sku_date": sku_date }
  }).done(function (data) {
    series_amount = [];
    series_hour = [];
    y_axis_amount = [];
    colors = [];
    init_brand = 0;
    max_brand = 0;
    var i = 0
    // PER HOUR
    Object.keys(data["brands"]).forEach(function (brand) {
      var brand_amount = data["brands"][brand]["amount"];
      var brand_count = data["brands"][brand]["count"];
      series_amount_push(brand, brand_amount);
      series_count_push(brand, brand_count);
      compute_max_brand(brand_amount, brand);
      colors.push(color_pallete[i]);
      i++;
    });
    create_yaxis();
    total_amt = data["totals"]["total_amt_hr"];
    total_cnt = data["totals"]["total_cnt_hr"];
    push_totals(total_amt, total_cnt);
    colors.push("#000000")
    chart_day.updateOptions({
      yaxis: y_axis_amount,
      colors: colors
    }
    );
    chart_day.updateSeries(series_amount);
  });
}

$.ajax({
    url: "/topsku_day_js",
    method: "GET",
    dataType: "json"
}).done(function (data) {
  var i = 0;
  // PER HOUR
  Object.keys(data["brands"]).forEach(function (brand) {
    var brand_amount = data["brands"][brand]["amount"];
    var brand_count = data["brands"][brand]["count"];
    series_amount_push(brand, brand_amount);
    series_count_push(brand, brand_count);
    compute_max_brand(brand_amount, brand);
    colors.push(color_pallete[i]);
    i++;
  });
  create_yaxis();
  total_amt = data["totals"]["total_amt_hr"];
  total_cnt = data["totals"]["total_cnt_hr"];
  push_totals(total_amt, total_cnt);
  colors.push("#000000")
  var options = {
    chart: {
      height: 350,
      type: 'line',
      stacked: false
    },
    dataLabels: {
      enabled: false,
    },
    colors: colors,
    series: series_amount,
    stroke: {
      show: true,
      width: 2,
      curve: 'smooth'
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '70%',
        endingShape: 'rounded'
      },
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
      categories: ['0500H', '0900H', '1300H', '1700H', '2100H', '0100H'],
      tickPlacement: 'between'
    },
    yaxis: y_axis_amount
  };

  chart_day = new ApexCharts(document.querySelector("#topsku_day"), options);
  chart_day.render();
});



