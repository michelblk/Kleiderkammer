$(function () {
    $(document).on('shown.bs.modal', '#mitglied-details', function (e) {
        const mitgliedId = $("#mitglied-details .modal").data("mitglied-id");

        requestAktuelleKleidung(mitgliedId, updateAktuelleKleidung, () => {

        });
    });
});

function requestAktuelleKleidung(mitgliedId, success, failure) {
    $.ajax({
        cache: false,
        data: {
            mitgliedId: mitgliedId
        },
        method: 'GET',
        success: success,
        failure: failure,
        url: "{{ url_for('kleidung_api.aktuelle_kleidung') }}"
    });
}

function updateAktuelleKleidung(kleidung) {
    const templateObj = $("#aktuelle-kleidung-row-template");

    const rowTemplate = Handlebars.compile(templateObj.html());

    $("#aktuelle-kleidung-table tbody").html(rowTemplate(kleidung));
}