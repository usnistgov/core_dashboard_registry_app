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

/**
 * Update URL
 */
get_url = function(ispublished, page) {
    var url = urlResources;
    var published = '';
    var list_role = '';
    var i = 0;

    // Get list of selected roles
    $('input:checked[name=my_role]').each(function() {
        if (i > 0) {
            list_role += '&';
        }
        list_role += 'role='+$(this).val();
        i++;
    });

    // Check if publish or not published
    if (ispublished == 'true') {
        published = 'ispublished=true';
    } else if (ispublished == 'false') {
        published = 'ispublished=false';
    }

    // Update URL with roles, publish and page
    if (list_role != '') {
        url += '?'+list_role;
        if (published != '') {
            url += '&' + published;
        } if (page != '' && page != '1') {
            url += '&page=' + page;
        }
    } else if (published != '') {
        url += '?' + published;
        if (page != '' && page != '1') {
            url += '&page=' + page;
        }
    } else if (page != '' && page != '1') {
        url += '?page=' + page;
    }
    window.location.href = url;
};
