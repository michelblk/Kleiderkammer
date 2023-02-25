$(function () {
    $(document).on("shown.bs.modal", "#mitglied-details", function (e) {
        const mitgliedId = $("#mitglied-details .modal").data("mitglied-id");

        requestAktuelleKleidung(mitgliedId, updateAktuelleKleidung, () => {});
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
                url: "{{ url_for('mitglieder_api.entfernen', mitglied_id='_mitglied_id_') }}".replace(
                    "_mitglied_id_",
                    mitglied_id
                ),
            });
        }
    });
});

function requestAktuelleKleidung(mitgliedId, success, failure) {
    $.ajax({
        cache: false,
        data: {
            mitgliedId: mitgliedId,
        },
        method: "GET",
        success: success,
        failure: failure,
        url: "{{ url_for('kleidung_api.aktuelle_kleidung') }}",
    });
}

function updateAktuelleKleidung(kleidung) {
    const templateObj = $("#aktuelle-kleidung-row-template");

    const rowTemplate = Handlebars.compile(templateObj.html());

    $("#aktuelle-kleidung-table tbody").html(rowTemplate(kleidung));
}
