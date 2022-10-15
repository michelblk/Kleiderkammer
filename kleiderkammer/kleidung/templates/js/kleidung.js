'use strict';

function getActiveFiltersForColumn(column) {
    return $(`.filter[data-column='${column}']:checked`).map(function () {
        return $(this).val();
    }).get();
}

function filter(column, row, allowedValues) {
    const actualValue = row.find(`[data-column="${column}"]`).text();
    return allowedValues.length === 0 || allowedValues.some(val => {
        return actualValue.indexOf(val) > -1;
    })
}

$(function () {
    $(".filter").change(function () {
        const kategorieFilter = getActiveFiltersForColumn('kategorie');
        const herstellerFilter = getActiveFiltersForColumn('hersteller');
        const modellFilter = getActiveFiltersForColumn('modell');
        const groesseFilter = getActiveFiltersForColumn('groesse');
        const jahrFilter = getActiveFiltersForColumn('jahr');

        $("#kleidungstabelle tr").each(function () {
            const row = $(this);
            $(this).toggle(
                filter('kategorie', row, kategorieFilter)
                && filter('hersteller', row, herstellerFilter)
                && filter('modell', row, modellFilter)
                && filter('groesse', row, groesseFilter)
                && filter('jahr', row, jahrFilter)
            );
        });
    });

    const templateObj = $("#kleidung-details-template");
    const template = Handlebars.compile(templateObj.html());
    $(".kleidung").click(function () {
        const id = $(this).data('id');
        const code = $(this).find('[data-column="code"]').text();
        const kategorie = $(this).find('[data-column="kategorie"]').text();

        const target_object = $("#kleidung-details");
        target_object.attr('data-id', id);
        target_object.html(template({
            title: `${kategorie} ${code}`
        }));

        const modal = new bootstrap.Modal(target_object.find(".modal"));
        modal.show();
    });
});