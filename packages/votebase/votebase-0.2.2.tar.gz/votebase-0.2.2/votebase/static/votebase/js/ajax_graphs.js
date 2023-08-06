$(document).ready(function() {
    var counter = 0;
    var num_questions = $(".statistics-list tr").length;

    $(".ajax-loader").css('display', 'block');
    $(".statistics-list table.table").css('display', 'none');
    $(".share_and_export").css('display', 'none');
    $(".statistics-voters-limit").css('display', 'none');

    $(".statistics-list tr").each(function(){
        var href = $(this).find(".title a").attr('href');
        var toLoad = href + " .statistics-item";
        $(this).attr('data', href);

        $(this).load(toLoad, function() {
             $(this).find('.star').rating();

            counter++;
            if(counter == num_questions) {
                $(".statistics-list table.table").css('border-collapse', 'collapse');
                $(".ajax-loader").css('display', 'none');
                $(".statistics-list table.table").css('display', 'table');
                $(".share_and_export").css('display', 'block');
                $(".statistics-voters-limit").css('display', 'block');

                $(".pagination ul li:not(.dots):not(.disabled) a").each(function(){
                    var href = $(this).closest("tr").attr('data');
                    var page = $(this).attr('href');
                    $(this).attr('href', href+page);
                });
            }
        });
    });
});