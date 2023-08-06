$(document).ready(function() {
    InitSurveyTitle();
    InitEzMark();
    InitOpenableNavs();
    InitQuestionKindsToggler();
    InitAccordion();
    InitSortableQuestions();
    InitSortableOptions();
    InitDatepicker();
    InitDatetimepicker();
    InitTimespinner();
    InitTabs();
    InitHelpBlocks();

    $('.image_icon').live('click', function() {
        $(this).toggleClass('open');
    });

    $('.category_icon').live('click', function() {
        $(this).toggleClass('open');
    });
});

function InitTabs() {
    $('.tabbed a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    if (window.location.hash) {
        $('a[href=' + window.location.hash + ']').tab('show');
    }

    $('.segments-info .edit').on({
        'click': function() {
            if (window.location.hash) {
                $('a[href=' + $(this).attr('rel') + ']').tab('show');
            }
        }
    });
}

function InitDatetimepicker() {
    $.widget( 'ui.timespinner' , $.ui.spinner, {
        options: {
            // seconds
            step: 60 * 1000,
            // hours
            page: 60
        },

        _parse: function( value ) {
            if ( typeof value === 'string' ) {
                // already a timestamp
                if ( Number( value ) == value ) {
                    return Number( value );
                }
                return +Globalize.parseDate( value );
            }
            return value;
        },

        _format: function( value ) {
            return Globalize.format( new Date(value), "t" );
        }
    });

    Globalize.culture('sk-SK');
    $('.splitdatetimewidget').each(function() {
//        $('input[type=text]', this).eq(0).datepicker({
//            dateFormat: 'yy-mm-dd'
//        });
        $('input[type=text]', this).eq(0).pickadate({
            format: 'yyyy-mm-dd',
            formatSubmit: 'yyyy-mm-dd'
        });
        $('input[type=text]', this).eq(1).timespinner();
    });
}

function InitDatepicker() {
    $('.datepicker').pickadate({
        format: 'yyyy-mm-dd',
//        format: 'dd. mmmm yyyy',
        formatSubmit: 'yyyy-mm-dd',
        selectYears: 100,
        selectMonths: true,
        firstDay: 1
    });

//    $('.datepicker').pickadate({
//        format: 'dd.mm.yyyy',
//        formatSubmit: 'dd.mm.yyyy',
//        firstDay: 1
//    });

    //    $('.datepicker').datepicker({
//        dateFormat: 'yy-mm-dd'
//    });
}

function InitTimespinner() {
    $('.timespinner').timespinner();
}

function InitSortableQuestions() {
    $('.questions-list').sortable({
        axis: 'y',
        handle: '.move',
        items: '.question',
        placeholder: 'placeholder',
        start: function(event, ui) {
            $('.questions-list').addClass('sorting');
            ui.placeholder.html('Your question will be here.');
        },
        stop: function(event, ui) {
            $('.questions-list').removeClass('sorting');
        },
        update: function(event, ui) {
            var order = [];

            $('.questions-list .question').each(function(index) {
                $('.counter .number', this).text(index + 1);
            });

            $('.questions-list .question').each(function(index, element) {
                order.push(parseInt($(this).attr('rel')));
            });

            $.ajax({
                url: $('.question-list').attr('rel'),
                type: 'POST',
                data: {order: order},
                success: function(data) {}
            });
        }
    });
}

function InitSortableOptions() {
    $('.question-admin .options').sortable({
        axis: 'y',
        handle: '.move',
        items: '.wrapper',
        update: function(event, ui) {
            $('.question-admin .formset-item').each(function(index) {
                $('.order', this).attr('value', index);
            });
        }
    })
}

function InitAccordion() {
    $('.accordion .accordion-body.in').closest('.accordion-group').find('.accordion-heading a').addClass('active');
    $('.accordion').on('show', function (e) {
        $(e.target).prev('.accordion-heading').find('.accordion-toggle').addClass('active');
    });

    $('.accordion').on('hide', function (e) {
        $(this).find('.accordion-toggle').not($(e.target)).removeClass('active');
    });
}

function InitOpenableNavs() {
    $('ul.openable').each(function(index) {
        $('li.active', this).closest('ul').removeClass('closed');
    });

    $('ul.openable li.nav-header').live('click', function() {
        $(this).closest('ul').toggleClass('closed');
    });
}

function InitQuestionKindsToggler() {
    $('#sidebar-questions .nav.advanced .nav-header').click(function(){
        $('#sidebar-questions .nav.advanced .item').slideToggle();
    });
}

function InitEzMark() {
    $('input[type="checkbox"]').ezMark();

    $('input[type="radio"]:not(.star)').ezMark();
    $('select:not(.disable-chosen)').chosen({ "disable_search_threshold": 50 });
}

function InitSurveyTitle() {
    $('input.survey-title').live('focusout', function(){
        var input = $(this);
        var form = $(this).closest('form');
        form.submit();
        // $.ajax({
        //     url: form.attr('action'),
        //     data: form.serialize(),
        //     type: 'POST'
        // });
    });
}

function InitHelpBlocks() {
    // Popover
    $('.help-block').each(function(index) {
        $(this).popover({
            'html' : true,
            'trigger': 'hover',
            'placement': 'right',
            'delay': { 'show': 100, 'hide': 1000 }
        });
    });
}