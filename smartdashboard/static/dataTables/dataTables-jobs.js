$(document).ready(function() { 
    var min
    var max 
    jQuery(function(){
        jQuery('#min').datetimepicker({
         onShow:function( ct ){
          this.setOptions({
           maxDate:jQuery('#max').val()?jQuery('#max').val():false
          })
         },
        onSelectTime:function(ct,$input){
            min = $input.val()
            console.log(min);
        },
         format:'Y-m-d H:i',
         maxDateTime:true,
        });

        jQuery('#max').datetimepicker({
         onShow:function( ct ){
          this.setOptions({
           minDate:jQuery('#min').val()?jQuery('#min').val():false
          })
         },
         onSelectTime:function(ct,$input){
            max = $input.val()
            console.log(max);
        },
         format:'Y-m-d H:i',
         maxDateTime:true,
        }); 
    });




}) 

