$(function() {

    $( document ).ready(function() {

        if ($("#compare-view").length) {
            $("#main-content").removeClass("col-sm-8");
            $("#main-content").addClass("col-sm-12");
        }

        $( ".workout-log" ).each(function() {
          var elem = this;
          log_url = $( this ).attr('data-url');
          $.ajax(log_url).done(function(data) {
                var data_obj = $(data).find("#content");
                // Delete Add log buttons from the html
                $(data_obj).find(".btn-success").remove();
                $(elem).html(data_obj);
            })

        });
        $(".exercise-filter").click(function() {
            var hash = $(this).find('a').attr('href').split("#")[1];
            filterExercises(hash)
        });

        $("#show-all-exercises").click(function() {
            $(".list-group .workout-item").show();
        });

    });

    function filterExercises(property) {

        var exercise = false;
        var member = false;

        if (property.indexOf("ex-") == 0) {
            exercise = property.split("ex-")[1];
            var div = $(".log-div").find("a").filter(function( index ) {
                var href = $( this ).attr( "href" );
                var hr =  href.split("/").pop()
                var elem = false;

                if (exercise === hr){
                    elem = href
                    }
                return elem.length > 0;
              })

            var parent_log_div = $(div).parents(".log-div");
            var parent_list_group = $(div).parents(".list-group-item");

            // Show everything first before hiding
            $('.log-div').show();
            $('.list-group-item').show();
            $('.log-div').not($(parent_log_div)).hide();
            $('.list-group-item').not($(parent_list_group)).hide();


            if($('#member-workouts .list-group').children(":visible").length
             == 0) {
               $("#no-exercises-match").css({
                    "display": "block",
                });
            } else {
                 $("#no-exercises-match").css({
                    "display": "none"
                });
            }

        } else if (property.indexOf("member-") == 0) {
            member = property.split("member-")[1];
            var div = $("#member-workouts .workout-item").find(
            "span.member-name").filter
            (function( index ) {
                var username = $(this).text();
                var elem = false;

                if (username.trim() === member){
                    elem = $(this)
                    }
                return elem.length > 0;
              })

            var parent = $(div).parents(".workout-item");

            // Show everything first before hiding
            $("#member-workouts .workout-item").show();
            $("#member-workouts .workout-item").not($(parent)).hide();

            if (parent.html() === undefined) {
                $("#no-exercises-match").css({
                    "display": "none"
                });
                $("#no-member-match").css({
                    "display": "block"
                });

            } else {
                $("#no-exercises-match").css({
                    "display": "none"
                });
                 $("#no-member-match").css({
                    "display": "none"
                });
            }
        }

    }
})
