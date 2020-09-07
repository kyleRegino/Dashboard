$('#cdr_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
});

$("#cdr_date_form_hive").submit(function(event){
    event.preventDefault();
    var cdr_date = $("#cdr_date").val();
    $.ajax({
        url: "/dqchecks_manvshive_search",
        method: "POST",
        data: { "date": cdr_date}
    }).done(function(data){
        $("#variance_com").text(data.variance_com);
        $("#variance_cm").text(data.variance_cm);
        $("#variance_vou").text(data.variance_vou);
        $("#variance_adj").text(data.variance_adj);
        $("#variance_first").text(data.variance_first);
        $("#variance_mon").text(data.variance_mon);
        $("#variance_data").text(data.variance_data);
        $("#variance_voice").text(data.variance_voice);
        $("#variance_sms").text(data.variance_sms);
        $("#variance_clr").text(data.variance_clr);
        update_data_hive(cdr_date);
        update_colors();
    });

});

$("#cdr_date_form_oracle").submit(function (event) {
    event.preventDefault();
    var cdr_date = $("#cdr_date").val();
    $.ajax({
        url: "/dqchecks_manvsoracle_search",
        method: "POST",
        data: { "date": cdr_date }
    }).done(function (data) {
        $("#variance_com").text(data.variance_com);
        $("#variance_cm").text(data.variance_cm);
        $("#variance_vou").text(data.variance_vou);
        $("#variance_adj").text(data.variance_adj);
        $("#variance_first").text(data.variance_first);
        $("#variance_mon").text(data.variance_mon);
        $("#variance_data").text(data.variance_data);
        $("#variance_voice").text(data.variance_voice);
        $("#variance_sms").text(data.variance_sms);
        $("#variance_clr").text(data.variance_clr);
        update_data_oracle(cdr_date);
        update_colors();
    });

});

function update_colors(){
    if (parseInt($("#variance_com").text().replace(/,/g, "")) != 0) {
        $("#variance_com").css("color", "red");
    }
    else {
        $("#variance_com").css("color", "black");
    }
    if (parseInt($("#variance_vou").text().replace(/,/g, "")) != 0) {
        $("#variance_vou").css("color", "red");
    }
    else {
        $("#variance_vou").css("color", "black");
    }
    if (parseInt($("#variance_first").text().replace(/,/g, "")) != 0) {
        $("#variance_first").css("color", "red");
    }
    else {
        $("#variance_first").css("color", "black");
    }
    if (parseInt($("#variance_mon").text().replace(/,/g, "")) > 20000 || parseInt($("#variance_mon").text().replace(/,/g, "")) < -20000) {
        $("#variance_mon").css("color", "red");
    }
    else {
        $("#variance_mon").css("color", "black");
    }
    if (parseInt($("#variance_cm").text().replace(/,/g, "")) > 10000 || parseInt($("#variance_cm").text().replace(/,/g, "")) < -10000) {
        $("#variance_cm").css("color", "red");
    }
    else {
        $("#variance_cm").css("color", "black");
    }
    if (parseInt($("#variance_adj").text().replace(/,/g, "")) > 10000 || parseInt($("#variance_adj").text().replace(/,/g, "")) < -10000) {
        $("#variance_adj").css("color", "red");
    }
    else {
        $("#variance_adj").css("color", "black");
    }
}

$("document").ready(function () {
    update_colors();
});