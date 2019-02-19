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
    if (ispublished === 'true') {
        published = 'ispublished=true';
    } else if (ispublished === 'false') {
        published = 'ispublished=false';
    }

    // Update URL with roles, publish and page
    if (list_role !== '') {
        url += '?'+list_role;
        if (published !== '') {
            url += '&' + published;
        } if (page !== '' && page !== '1') {
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