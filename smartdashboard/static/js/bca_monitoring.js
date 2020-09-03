$.ajax({
    url: "/get_bca_monitoring",
    method: "GET",
    dataType: "json"
}).done(function (data) {
    console.log(data);
    var options = {
        series: [
            {
                name: "Usagetype Total",
                data: data["usagetype_total"]
            },
            {
                name: "Prp Account",
                data: data["prp_acct"]
            },
            {
                name: "Pcodes",
                data: data["pcodes"]
            },
            {
                name: "UsageType_DataDeducts",
                data: data["data_deducts"]
            },
            {
                name: "UsageType_Expiration",
                data: data["expiration"]
            },
            {
                name: "UsageType_TopupDeducts",
                data: data["topup_deducts"]
            },
            {
                name: "UsageType_VoiceDeducts",
                data: data["voice_deducts"]
            },
            {
                name: "UsageType_VasDeducts",
                data: data["vas_deducts"]
            },
            {
                name: "UsageType_SMSDeducts",
                data: data["sms_deducts"]
            }
        ],
        chart: {
            height: 700,
            type: 'line',
            dropShadow: {
                enabled: true,
                color: '#000',
                top: 18,
                left: 7,
                blur: 10,
                opacity: 0.2
            },
            zoom: {
                enabled: true,
                type: 'x',  
                autoScaleYaxis: false,  
                zoomedArea: {
                  fill: {
                    color: '#90CAF9',
                    opacity: 0.4
                  },
                  stroke: {
                    color: '#0D47A1',
                    opacity: 0.4,
                    width: 1
                  }
                }
            },
            toolbar: {
                show: true,
                autoSelected: 'zoom'
              }
        },
        colors: ['#77B6EA', '#545454', "#00E676", "#FFEA00", "#FFA06D", "#718792", "#D50000", "#D500F9", "#1A237E", "#4E342E"],
        dataLabels: {
            enabled: false,
            formatter: function (value) {
                return new Date(value * 1000).toISOString().substr(11, 8);
            }
        },
        stroke: {
            curve: 'smooth'
        },
        // title: {
        //     text: 'BCA Jobs Duration per Day',
        //     align: 'left'
        // },
        title: {
            text: 'BCA Jobs Duration per Day',
            align: 'left',
            margin: 50,
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
        grid: {
            borderColor: '#e7e7e7',
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        markers: {
            size: 1,
            color: '#263238'
        },
        xaxis: {
            categories: data["dates"],
            title: {
                text: 'Date'
            }
        },
        yaxis: {
            title: {
                text: 'Duration'
            },
            labels: {
                formatter: function (value) {
                    return new Date(value * 1000).toISOString().substr(11, 8);
                }
            }
            // min: 5,
            // max: 40
        },
        legend: {
            position: 'top',
            horizontalAlign: 'center',
            floating: true,
            offsetY: -25,
            offsetX: -5
        }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
});



