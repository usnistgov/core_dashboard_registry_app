$(document).ready(function(){
    initRole(roles);
});

initRole = function (roles_list) {
    var btns = $("#my_role").children("input");
    for(var i = 0; i < btns.length; i++) {
        // when value change
        btns[i].onclick = function () {
            var selected_val = $(this).val();
            var td = $("#td_"+selected_val);
            if ($(this).prop('checked') == true) {
                td.addClass("selected_resource");
            } else {
                td.removeClass("selected_resource");
            }
        };
    }

    if (roles_list != "") {
        roles_list = roles_list.split(',');
        for (var i = 0 ; i<roles_list.length; i++) {
            click_role(roles_list[i]);
        }
    }
};


/**
 * Check if all the images are selected
 * @returns {boolean}
 */
is_all_td_selected = function() {
    return $("#Organization").prop('checked') == true
        && $("#Dataset").prop('checked') == true
        && $("#DataCollection").prop('checked') == true
        && $("#ServiceAPI").prop('checked') == true
        && $("#Software").prop('checked') == true
        && $("#WebSite").prop('checked') == true ;
};

/**
 * Click for a role
 */
click_role = function(role) {
    if (role == 'all') {
        $("#my_role").find('input:checked').prop('checked', false);
        $("#td_" + role).addClass("selected_resource");
    } else {
        $("#td_all").css({'class': ''});
        $("#"+role).click();
        if (is_all_td_selected()) {
            $("#my_role").find('input:checked').prop('checked',false);
            $("#td_" + role).removeClass("selected_resource");
        }
    }
};
