"use strict";

$(function () {
    const templateObj = $("#mitglied-details-template");
    const template = Handlebars.compile(templateObj.html());
    $(".mitglied").click(function () {
        const mitgliedId = $(this).data("id");
        const vorname = $(this).find("[data-column='vorname']").text();
        const nachname = $(this).find("[data-column='nachname']").text();

        const target_object = $("#mitglied-details");
        target_object.html(
            template({
                title: `${nachname}, ${vorname}`,
                mitgliedId: mitgliedId,
            })
        );

        const modal = new bootstrap.Modal(target_object.find(".modal"));
        modal.show();
    });
});
