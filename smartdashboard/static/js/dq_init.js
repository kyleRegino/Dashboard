$('#cdr_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
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