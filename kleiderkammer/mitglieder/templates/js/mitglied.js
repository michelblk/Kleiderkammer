$(function () {

    const templateObj = $("#mitglied-details-template");
    const template = Handlebars.compile(templateObj.html());
    $(".mitglied").click(function () {
        const mitgliedId = $(this).parent('tr').data('id'); // TODO fix

        const target_object = $("#mitglied-details");
        target_object.data('id', mitgliedId);
        target_object.html(template({
            title: 'test'
        }));
    });
});