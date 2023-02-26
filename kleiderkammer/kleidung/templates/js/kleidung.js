"use strict";

function getActiveFiltersForColumn(column) {
    return $(`.filter[data-column='${column}']:checked`)
        .map(function () {
            return $(this).val();
        })
        .get();
}

function filter(column, row, allowedValues) {
    const actualValue = row.find(`[data-column="${column}"]`).text();
    return (
        allowedValues.length === 0 ||
        allowedValues.some((val) => {
            return actualValue === val;
        })
    );
}

$(function () {
    $(".filter").change(function () {
        filterKleidungstabelle();
    });

    const templateObj = $("#kleidung-details-template");
    const template = Handlebars.compile(templateObj.html());
    $(document).on("click", ".kleidung", function () {
        const id = $(this).data("id");
        const code = $(this).find('[data-column="code"]').text();
        const kategorie = $(this).find('[data-column="kategorie"]').text();

        const target_object = $("#kleidung-details");
        target_object.attr("data-id", id);
        target_object.html(
            template({
                title: `${kategorie} ${code}`,
                kleidungId: id,
            })
        );

        const modal = new bootstrap.Modal(target_object.find(".modal"));
        modal.show();

        target_object.find(".modal").on("hidden.bs.modal", function () {
            refreshKleidungstabelle();
        });
    });
});

function filterKleidungstabelle() {
    const kategorieFilter = getActiveFiltersForColumn("kategorie");
    const herstellerFilter = getActiveFiltersForColumn("hersteller");
    const modellFilter = getActiveFiltersForColumn("modell");
    const groesseFilter = getActiveFiltersForColumn("groesse");
    const jahrFilter = getActiveFiltersForColumn("jahr");
    const waeschenFilter = getActiveFiltersForColumn("waeschen");

    $("#kleidungstabelle tr").each(function () {
        const row = $(this);
        $(this).toggle(
            filter("kategorie", row, kategorieFilter) &&
                filter("hersteller", row, herstellerFilter) &&
                filter("modell", row, modellFilter) &&
                filter("groesse", row, groesseFilter) &&
                filter("jahr", row, jahrFilter) &&
                filter("waeschen", row, waeschenFilter)
        );
    });
}

function refreshKleidungstabelle() {
    $.ajax({
        url: "",
        method: "GET",
        success: function (data) {
            const newKleidungstabelle = $(data).find("#kleidungstabelle:first").html();
            $("#kleidungstabelle").html(newKleidungstabelle);
            filterKleidungstabelle();
        },
    });
}
