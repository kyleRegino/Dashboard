$("document").ready(function(){
    $(window).on('load resize', function(){
        $('.div').width($(this).width());
    });
});