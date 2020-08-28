$("#cdr_date_form_hive").submit(function(event){
    event.preventDefault();
    var cdr_date = $("#cdr_date").val();
    $.ajax({
        url: "/dq_checks_search_hive",
        method: "POST",
        data: { "date": cdr_date}
    }).done(function(data){
        $("#variance_com").text(data.variance_com);
        $("#variance_cm").text(data.variance_cm);
        $("#variance_vou").text(data.variance_vou);
        $("#variance_adj").text(data.variance_adj);
        $("#variance_first").text(data.variance_first);
        $("#variance_mon").text(data.variance_mon);
        update_data_hive(cdr_date);
    });

});

$("#cdr_date_form_oracle").submit(function (event) {
    event.preventDefault();
    var cdr_date = $("#cdr_date").val();
    $.ajax({
        url: "/dq_checks_search_oracle",
        method: "POST",
        data: { "date": cdr_date }
    }).done(function (data) {
        $("#variance_com").text(data.variance_com);
        $("#variance_cm").text(data.variance_cm);
        $("#variance_vou").text(data.variance_vou);
        $("#variance_adj").text(data.variance_adj);
        $("#variance_first").text(data.variance_first);
        $("#variance_mon").text(data.variance_mon);
        update_data_oracle(cdr_date);
    });

});