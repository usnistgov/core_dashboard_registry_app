$(document).ready(function(){

    var divs = $("#icons_banner div");
    for (var i=0; i<divs.length; i++) {
        divs[i].onclick = function () {
            var id = this.id.replace('cnt_','');
            action_click(id);
        };
    }

    if (roles != "") {
        roles = roles.split(',');
        for (var i = 0 ; i<roles.length; i++) {
            click_role(roles[i]);
        }
    }

});


/**
 * Check if all the images are selected
 * @returns {boolean}
 */
is_all_td_selected = function() {
    var list_roles = list_role_custom_resource.split(',');
     for (var i = 0 ; i<list_roles.length; i++) {
      if(!$("#cnt_" + list_roles[i]).hasClass('selected_resource')){
          return false;
      }
    }
    return true;
};

/**
 * Click for a role
 */
click_role = function(role) {

    if ($("#cnt_" + role).hasClass("selected_resource")) {
        $("#cnt_" + role).removeClass("selected_resource");
    } else {
        $("#cnt_" + role).addClass("selected_resource");
        if (role != role_custom_resource_type_all) {
             $("#cnt_"+ role_custom_resource_type_all).removeClass('selected_resource')
        }
        if (role == role_custom_resource_type_all || is_all_td_selected()) {
            var list_roles = list_role_custom_resource.split(',');
            for (var i = 0 ; i<list_roles.length; i++) {
                $("#cnt_" + list_roles[i]).removeClass('selected_resource');
            }
            $("#cnt_"+ role_custom_resource_type_all).addClass('selected_resource')
        }
    }
};

/**
 * Action click
 */
action_click = function(action) {
    click_role(action);
    get_url(published, '');
};