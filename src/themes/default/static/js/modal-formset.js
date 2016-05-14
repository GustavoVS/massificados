$('.add-to-formset').click(function(){

    var next_id = 0;
    $('#'+ $(this).attr('formset-id') + ' .formset-group').each(function(){
        if($(this).attr('formset-seq-id') > next_id )
            next_id = $(this).attr('formset-seq-id')
    });

    next_id++;
    var clone_formset = $('#'+ $(this).attr('default-formset'))
        .clone()
        .html()
        .replace(/__prefix__/g, "" + next_id );

//    $('#'+ $(this).attr('formset-id') ).append($(clone_formset).html(clone_formset));

});

$('').click(function(){});

$('').click(function(){});

$('').click(function(){});

$('').click(function(){});

$('').click(function(){});

$('').click(function(){});

$('').click(function(){});
