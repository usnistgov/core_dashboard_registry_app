/*
*   Javascript function for registry record list
*/

// function that switch the status
function switchStatus(data_id, old_status, new_status, btn_element){
    // actions only if the status change
    if (old_status !== new_status) {
        $.ajax({
            url : switchStatusRecordUrl,
            type : "POST",
            data: {
                "data_id": data_id,
                "new_status": new_status
            },
            success: function(data){
                btn_element.attr('class', 'dropbtn status-' + new_status);
                btn_element.attr('data-status', new_status);
                btn_element.closest('td').children('span.label-status').attr('class', 'float-right label-status font-'+ new_status);
                btn_element.closest('td').children('span.label-status').text(new_status);
            },
            error: function(data) {
                var errors = $.parseJSON(data.responseText);
                $.notify(errors.message, {style: 'error'});
            }
        });
    }
}

// called when the webpage is loaded
$(document).ready(function() {
    $('.switch').each(function() {
        // bind the click event to switch the status
        $(this).bind("click", function(e) {
            switchStatus(
                // data_id
                $(this).closest('tr').attr('objectid'),
                // old_status
                $(this).closest('span').children('.dropbtn').attr('data-status'),
                // new_status
                $(this).attr('data-status'),
                // btn_element
                $(this).closest('span').children('.dropbtn')
            );
        });
    });
});
