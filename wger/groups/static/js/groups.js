$(function() {

$( document ).ready(function() {
    $( ".workout-log" ).each(function() {
      log_url = $( this ).attr('data-url');
      console.log("UrL: " + log_url);

    });
});

})
