 $(document).ready(function() {
    $("#dataTable").find("tr").each(function () {
        var duration= $(this).find(".duration"); 
        console.log(duration);
        if(duration.html() >= 30.00)
          {
            $(duration).addClass("text-danger");
          }
    
       var status= $(this).find(".status");
       console.log(status);
       if(status.html() == 'RUNNING')
       {
        $(status).addClass('badge badge-warning')
       }
       if (status.html() == 'OK') 
       {
        // $(status).innerHTML = "COMPLETED";
        $(status).html("COMPLETED");
        $(status).addClass('badge badge-success')
       }
       if (status.html() == 'ERROR') {
        $(status).addClass('badge badge-danger')
       }
       if (status.html() == 'MISFIRED') {
        $(status).addClass('badge badge-info')
       }
    });


    $(".main-panel").each(function () {
      var current_status= $(this).find("#current_status"); 
      console.log(current_status.html());
      if(current_status.html() == 'RUNNING JOBS') {
        var running_card=$(this).find('#running_card')
        $(running_card).fadeTo('slow',.6);
        $(running_card).append('<div style="position: absolute;top:0;left:0;width: 100%;height:100%;z-index:2;opacity:0.4;filter: alpha(opacity = 50)"></div>');
      }
      if (current_status.html() == 'OK JOBS') {
        var ok_card=$(this).find('#ok_card')
        $(ok_card).fadeTo('slow',.6);
        $(ok_card).append('<div style="position: absolute;top:0;left:0;width: 100%;height:100%;z-index:2;opacity:0.4;filter: alpha(opacity = 50)"></div>');
      }
      if (current_status.html() == 'ERROR JOBS') {
        var error_card=$(this).find('#error_card')
        $(error_card).fadeTo('slow',.6);
        $(error_card).append('<div style="position: absolute;top:0;left:0;width: 100%;height:100%;z-index:2;opacity:0.4;filter: alpha(opacity = 50)"></div>');
      }
      if (current_status.html() == 'MISFIRED JOBS') {
        var misfired_card=$(this).find('#misfired_card')
        $(misfired_card).fadeTo('slow',.6);
        $(misfired_card).append('<div style="position: absolute;top:0;left:0;width: 100%;height:100%;z-index:2;opacity:0.4;filter: alpha(opacity = 50)"></div>');
      }

    });

    $("#lrj_csv").click(function(){
      $("#lrj_modal_csv").modal("hide");
    });

    $("#lrj_excel").click(function(){
      $("#lrj_modal_excel").modal("hide");
    });

});