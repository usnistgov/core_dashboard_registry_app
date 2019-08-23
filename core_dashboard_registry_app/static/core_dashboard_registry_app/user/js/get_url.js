/**
 * Update URL
 */
get_url = function (ispublished, page) {
    var url = urlResources;
    var published = '';
    var list_role = '';


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
        published = 'ispublished=true';
    } else if (ispublished === 'false') {
        published = 'ispublished=false';
    }

    // Update URL with roles, publish and page
    if (list_role !== '') {
        url += '?' + list_role;
        if (published !== '') {
            url += '&' + published;
        }
        if (page !== '' && page !== '1') {
            url += '&page=' + page;
        }
    } else if (published !== '') {
        url += '?' + published;
        if (page !== '' && page !== '1') {
            url += '&page=' + page;
        }
    } else if (page !== '' && page !== '1') {
        url += '?page=' + page;
    }
    window.location.href = url;
};