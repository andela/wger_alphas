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
        $(".exercise-filter").click(function() {
            var hash = $(this).find('a').attr('href').split("#")[1];
            console.log("Hash:  " + hash);
            filterExercises(hash)
        });

    });

    function filterExercises(property) {

        console.log("Filtering ");
        var exercise = false;
        var member = false;
        if (property.indexOf("ex-") == 0) {
            exercise = property.split("ex-")[1];
        } else if (property.indexOf("member-") == 0) {
            member = property.split("member-")[1];
        }
        if (exercise) {
            console.log("Exercise: " + exercise);
        } else if (member) {
            console.log("Member: " + member);

        }
    }
})
