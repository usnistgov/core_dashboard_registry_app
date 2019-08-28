/**
 * Update URL
 */
get_url = function (ispublished, page) {
    var url = urlResources;
    var list_role = '';
    url_name = '' ;

    var list_roles = list_role_custom_resource.split(',');
    for (var i = 0; i < list_roles.length; i++) {
        if ($("#cnt_" + list_roles[i]).hasClass('selected_resource')) {
            if (list_role != ''){
                list_role += '&';
            }
            list_role += 'role=' + list_roles[i];
        }
    }

    // Check if publish or not published
    if (ispublished === 'true') {
        url_name = 'ispublished=true';
    } else if (ispublished === 'false') {
        url_name = 'ispublished=false';
    }
    else if (ispublished === 'draft') {
        url_name = 'ispublished=draft';
    }


    // Update URL with roles, publish and page
    if (list_role !== '') {
        url += '?' + list_role;
        if (url_name !== '') {
            url += '&' + url_name;
        }
        if (page !== '' && page !== '1') {
            url += '&page=' + page;
        }
    } else if (url_name !== '') {
        url += '?' + url_name;
        if (page !== '' && page !== '1') {
            url += '&page=' + page;
        }
    } else if (page !== '' && page !== '1') {
        url += '?page=' + page;
    }
    window.location.href = url;
};