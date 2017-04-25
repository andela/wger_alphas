$(function() {

$( document ).ready(function() {

    if ($("#compare-view").length) {
        $("#main-content").removeClass("col-sm-8");
        $("#main-content").addClass("col-sm-12");
    }
    $( ".workout-log" ).each(function() {
      var elem = this;
      log_url = $( this ).attr('data-url');
      console.log("URL: " + log_url);
      $.ajax(log_url).done(function(data) {
//            console.log("Ajax: " + html = $.parseHTML(data));
            var data_obj = $(data).find("#content");
            // Delete Add log buttons from the html
            $(data_obj).find(".btn-success").remove();
            $(elem).html(data_obj);
        })

    });
});

})
