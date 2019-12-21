$(function () {
    $('#ftable').dataTable({
        "paging": false,
        "order": []
    });
    $('#ftable_length, #ftable_info, #ftable_paginate').remove();
    $("#ftable_filter").remove();

    $("#searchInput").keyup(function () {
        const rows = $("#fbody").find("tr").hide();
        const data = this.value.split(" ");
        $.each(data, function (i, v) {
            rows.filter(`:contains('${v}')`).show();
        });
    });
});