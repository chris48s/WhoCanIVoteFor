


fallback.ready(['jQuery'], function() {
    console.log()

    if ($('#feedback_form input[name=found_useful]:checked').val() == undefined) {
        $("#feedback_form .comments_container").hide()
        $('#feedback_form input[name=found_useful]').click(function() {
            $("#feedback_form .comments_container").show()
        })
    }

});
