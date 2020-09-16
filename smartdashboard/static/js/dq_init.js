$('#cdr_date').datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
});

var com_thresh = 0;
var vou_thresh = 0;
var first_thresh = 0;
var mon_thresh = 0;
var cm_thresh = 0;
var adj_thresh = 0;
var data_thresh = 0;
var sms_thresh = 0;
var voice_thresh = 0;
var clr_thresh = 0;

$.ajax({
    url: "/dqchecks_update_threshold",
    type: "GET",
    success: function(data) {
        com_thresh = data["COM"]
        vou_thresh = data["VOU"]
        first_thresh = data["FIRST"]
        mon_thresh = data["MON"]
        cm_thresh = data["CM"]
        adj_thresh = data["ADJ"]
        data_thresh = data["DATA"]
        sms_thresh = data["SMS"]
        voice_thresh = data["VOICE"]
        clr_thresh = data["CLR"]
    }
})

function update_colors(){
    if (parseInt($("#variance_com").text().replace(/,/g, "")) != com_thresh) {
        $("#variance_com").css("color", "red");
    }
    else {
        $("#variance_com").css("color", "black");
    }
    if (parseInt($("#variance_vou").text().replace(/,/g, "")) != vou_thresh) {
        $("#variance_vou").css("color", "red");
    }
    else {
        $("#variance_vou").css("color", "black");
    }
    if (parseInt($("#variance_first").text().replace(/,/g, "")) != first_thresh) {
        $("#variance_first").css("color", "red");
    }
    else {
        $("#variance_first").css("color", "black");
    }
    if (parseInt($("#variance_mon").text().replace(/,/g, "")) > mon_thresh || parseInt($("#variance_mon").text().replace(/,/g, "")) < -mon_thresh) {
        $("#variance_mon").css("color", "red");
    }
    else {
        $("#variance_mon").css("color", "black");
    }
    if (parseInt($("#variance_cm").text().replace(/,/g, "")) > cm_thresh || parseInt($("#variance_cm").text().replace(/,/g, "")) < -cm_thresh) {
        $("#variance_cm").css("color", "red");
    }
    else {
        $("#variance_cm").css("color", "black");
    }
    if (parseInt($("#variance_adj").text().replace(/,/g, "")) > adj_thresh || parseInt($("#variance_adj").text().replace(/,/g, "")) < -adj_thresh) {
        $("#variance_adj").css("color", "red");
    }
    else {
        $("#variance_adj").css("color", "black");
    }
    if (parseInt($("#variance_data").text().replace(/,/g, "")) > data_thresh || parseInt($("#variance_data").text().replace(/,/g, "")) < -data_thresh) {
        $("#variance_data").css("color", "red");
    }
    else {
        $("#variance_data").css("color", "black");
    }
    if (parseInt($("#variance_sms").text().replace(/,/g, "")) > sms_thresh || parseInt($("#variance_sms").text().replace(/,/g, "")) < -sms_thresh) {
        $("#variance_sms").css("color", "red");
    }
    else {
        $("#variance_sms").css("color", "black");
    }
    if (parseInt($("#variance_voice").text().replace(/,/g, "")) > voice_thresh || parseInt($("#variance_voice").text().replace(/,/g, "")) < -voice_thresh) {
        $("#variance_voice").css("color", "red");
    }
    else {
        $("#variance_voice").css("color", "black");
    }
    if (parseInt($("#variance_clr").text().replace(/,/g, "")) > clr_thresh || parseInt($("#variance_clr").text().replace(/,/g, "")) < -clr_thresh) {
        $("#variance_clr").css("color", "red");
    }
    else {
        $("#variance_clr").css("color", "black");
    }
}