/*
*   Javascript function for registry record
*/


// function that publish the data
function publish(data_id){
    var $registryRow = $(this).closest('tr');
    var objectID = $registryRow.attr("objectid");

    $.ajax({
        url : publishUrl,
        type : "POST",
        dataType: "json",
        data : {
            "data_id": objectID
        },
        success: function(data){
            location.reload(true);
        },
        error:function(data){
            var myArr = JSON.parse(data.responseText);
            $.notify(myArr.message, "danger");
        }
    });
}

$(".publish-record-btn").on('click', publish);
