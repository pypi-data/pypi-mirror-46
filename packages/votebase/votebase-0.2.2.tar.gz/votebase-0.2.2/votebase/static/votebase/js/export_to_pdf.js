function export_to_pdf(urlToPost, element) {
    $('#statistics_export_pdf').click(function(e){
        var form = $('<form></form>');
        var data = $(element).html();
        var input = $('<input type="hidden" />').attr('name','html').val(data);
        $(form).hide().attr('method','post').attr('action', urlToPost);
        $(form).append(input);
        $(form).appendTo('body').submit();
        e.preventDefault();
    });
}