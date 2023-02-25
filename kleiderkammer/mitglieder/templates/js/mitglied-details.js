$(function () {
    $(document).on("shown.bs.modal", "#mitglied-details", function (e) {
        const mitgliedId = $("#mitglied-details .modal").data("mitglied-id");

        requestKleidung(mitgliedId, updateKleidung, () => {});
    });

    // Mitglied löschen
    $(document).on("click", ".loeschen-button", function (e) {
        e.preventDefault();

        const mitglied_id = $("#mitglied-details .modal").data("mitglied-id");

        if (confirm("Wirklich löschen?")) {
            $.ajax({
                cache: false,
                method: "DELETE",
                success: function () {
                    // Entferne Zeile aus Tabelle und schließe Details
                    $(`.mitglied[data-id=${mitglied_id}]`).remove();
                    $("#mitglied-details").find(".modal").modal("hide");
                },
                url: "{{ url_for('mitglieder_api.entfernen', mitglied_id='_mitglied_id_') }}".replace("_mitglied_id_", mitglied_id),
            });
        }
    });
});

function requestKleidung(mitgliedId, success, failure) {
    $.ajax({
        cache: false,
        method: "GET",
        success: success,
        failure: failure,
        url: "{{ url_for('mitglieder_api.kleidung', mitglied_id='_mitglied_id_') }}".replace("_mitglied_id_", mitgliedId),
    });
}

function updateKleidung(kleidung) {
    const templateObj = $("#kleidung-row-template");

    const rowTemplate = Handlebars.compile(templateObj.html());

    $("#kleidung-table tbody").html(rowTemplate(kleidung));
}
