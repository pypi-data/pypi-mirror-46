function do_post(e) {
    e.preventDefault();
    current = $(e.target).closest('.modal-content');
    $(current).closest('.modal').modal('hide');
    $('#modalWait').modal('show');
    
    /* If it is null then the content should be loaded
    in the actual modal. */
    shell = $(this).attr('data-shell');
    if(shell == null) {
        shell = current;
    } 

    /* If it is null then the actual shell_error is supposed 
    to be a modal window. 
    Note: It is used just for HTTP 400 errors.*/
    shell_error = $(this).attr('data-shell-error');
    if(shell_error == null) {
        shell_error = current;
    } 

    callback_error = $(this).attr('data-callback-error');
    callback = $(this).attr('data-callback');

    url   = $(this).attr('data-show');
    form  = $(this).attr('data-form');

    var formData = new FormData($(form)[0]);

    $.ajax({
    url: url,  //Server script to process data
    type: 'POST',

    complete: function(jqXHR, textStatus) {
    switch (jqXHR.status) {

    case 200: 
    $('#modalWait').modal('hide');
    $(shell).html(jqXHR.responseText);
    eval(callback);

    $(shell).closest('.modal').modal('show');
    break;

    case 400: 
    $(shell_error).html(jqXHR.responseText);
    eval(callback_error);
    $('#modalWait').modal('hide');
    $(shell_error).closest('.modal').modal('show');
    break;

    default: 
    eval(callback_error);
    $('#modalWait').modal('hide');
    $('#messageError').html(jqXHR.responseText);
    $('#modalError').modal('show');
    $('#modalError').one('hidden.bs.modal', function () {
            $(shell_error).closest('.modal').modal('show');
        });
    }},

    data: formData,
    cache: false,
    contentType: false,
    processData: false
    });
}


function do_get(e) {
    e.preventDefault();
    current = $(e.target).closest('.modal-content');
    $(current).closest('.modal').modal('hide');
    $('#modalWait').modal('show');

    shell = $(this).attr('data-shell');

    if(shell == null) {
        shell = current;
    } 
    
    callback_error = $(this).attr('data-callback-error');
    callback = $(this).attr('data-callback');
    url   = $(this).attr('data-show');

    var lst = $(shell).data('stack');

    if(!lst) {
        lst = [];
        $(shell).data('stack', lst);
    } else if(!url) {
        lst.pop();
        [shell, url] = lst.pop();
    }

    $.ajax({
    url: url,  //Server script to process data
    type: 'GET',
    success: function(data) {
    $('#modalWait').modal('hide');
    eval(callback);
    
    $(shell).html(data);

    $(shell).closest('.modal').modal('show');
    lst.push([shell, url]);
    },

    error: function(data){
    eval(callback_error);
    $('#modalWait').modal('hide');
    $('#messageError').html(data.responseText);
    $('#modalError').modal('show');
    $('#modalError').one('hidden.bs.modal', function () {
            $(current).closest('.modal').modal('show');
        });
    },
    cache: false,
    contentType: false,
    processData: false
    });
}

$(document).on('click', '.e-get', do_get);
$(document).on('click', '.e-post', do_post);
$(document).on('click', '.r-post', do_post);

$(document).on('submit', 'form', function(e) {
    e.preventDefault();
    $('.e-post[data-form="#' + $(this).attr('id') + '"]').click();
});









