$(document).ready(function(){

    var tds = document.querySelectorAll("#icons_table td");
    for (var i=0; i<tds.length; i++) {
        tds[i].onclick = function () {
            var id = this.id.replace('td_','');
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
      if(!$("#td_" + list_roles[i]).hasClass('selected_resource')){
          return false;
      }
    }
    return true;
};

/**
 * Click for a role
 */
click_role = function(role) {

    if ($("#td_" + role).hasClass("selected_resource")) {
        $("#td_" + role).removeClass("selected_resource");
    } else {
        $("#td_" + role).addClass("selected_resource");
        if (role != role_custom_resource_type_all) {
             $("#td_"+ role_custom_resource_type_all).removeClass('selected_resource')
        }
        if (role == role_custom_resource_type_all || is_all_td_selected()) {
            var list_roles = list_role_custom_resource.split(',');
            for (var i = 0 ; i<list_roles.length; i++) {
                $("#td_" + list_roles[i]).removeClass('selected_resource');
            }
            $("#td_"+ role_custom_resource_type_all).addClass('selected_resource')
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