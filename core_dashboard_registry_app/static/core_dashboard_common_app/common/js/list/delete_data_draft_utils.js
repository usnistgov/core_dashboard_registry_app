/**
 * Strip the trailing ", Draft" label from a table row's name cell.
 *
 * @param {jQuery} btnObject - The button element containing the record.
 * @param {boolean} isAdminView - Zero-based index of the name cell within the row.
 */
removeDraftStatus = function(btnObject, isAdminView) {
    const $recordNameCol = btnObject.parents("table").find("tbody tr td").eq(0);
    $recordNameCol.find(".text-danger").remove();
    $recordNameCol.html($recordNameCol.html().replace(/,/, ''))
};
