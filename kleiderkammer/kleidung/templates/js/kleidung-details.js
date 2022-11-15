'use strict';

let mitgliedAuswaehlenDialog;

$(function () {
    // On load
    $(document).on('shown.bs.modal', '#kleidung-details', function (e) {
        refreshModal();
    });

    // Dialog events
    $(document).on('click', '.waschen-button', function (e) {
        e.preventDefault();
        const kleidung_id = $("#kleidung-details .modal").data('kleidung-id');
        const action = $(this).data('action');

        $.ajax({
            cache: false,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: {
                kleidung_id: kleidung_id,
                action: action
            },
            method: 'POST',
            success: function () {
                refreshModal();
            },
            url: "{{ url_for('kleidung_api.toggle_waesche') }}"
        });
    });

    $(document).on('click', '.verleihen-button[data-action="verleihen"]', function (e) {
        e.preventDefault();
        const kleidung_id = $("#kleidung-details .modal").data('kleidung-id');

        $.ajax({
            cache: false,
            method: 'GET',
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            success: function (mitglieder) {
                const dialogTemplateObj = $("#mitglied-auswaehlen-template");
                const dialogTemplate = Handlebars.compile(dialogTemplateObj.html());
                const dialogPlaceholder = $("#mitglied-dialog-placeholder");
                dialogPlaceholder.html(dialogTemplate({"kleidungId": kleidung_id, "mitglieder": mitglieder}));

                mitgliedAuswaehlenDialog = new bootstrap.Modal(dialogPlaceholder.find(".modal"));
                mitgliedAuswaehlenDialog.show();
            },
            url: "{{ url_for('mitglieder_api.get') }}"
        });
    });

    $(document).on('click', '.verleihen-button[data-action="zuruecknehmen"]', function (e) {
        e.preventDefault();

        const kleidung_id = $("#kleidung-details .modal").data('kleidung-id');

        $.ajax({
            cache: false,
            method: 'DELETE',
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: {
                "kleidungId": kleidung_id
            },
            success: function () {
                refreshModal();
            },
            url: "{{ url_for('kleidung_api.zuruecknehmen') }}"
        });
    });

    // Benutzer auswählen Events
    $(document).on('click', '.mitglied-waehlen', function (e) {
        e.preventDefault();

        const mitglied_id = $(this).data('mitglied-id');
        const kleidung_id = $(this).parents('[data-kleidung-id]').data('kleidung-id');

        $.ajax({
            cache: false,
            method: 'POST',
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: {
                "mitgliedId": mitglied_id,
                "kleidungId": kleidung_id
            },
            success: function () {
                mitgliedAuswaehlenDialog.hide();
                refreshModal();
            },
            url: "{{ url_for('kleidung_api.verleihen') }}"
        })
    });
});

function refreshModal() {
    const mitgliedId = $("#kleidung-details .modal").data("kleidung-id");

    requestAktuellenStatus(mitgliedId, updateKleidungsstatus, () => {
        alert("Kleidungsinformationen konnten nicht abgerufen werden.");
    });
}

function requestAktuellenStatus(kleidungId, success, failure) {
    $.ajax({
        cache: false,
        data: {
            kleidungId: kleidungId
        },
        method: 'GET',
        success: success,
        failure: failure,
        url: "{{ url_for('kleidung_api.status') }}"
    });
}

function updateKleidungsstatus(data) {
    const actionsTemplateObj = $("#kleidung-actions-template");
    const actionsTemplate = Handlebars.compile(actionsTemplateObj.html());
    const actions = $("#kleidung-actions");

    actions.html(actionsTemplate(data));
}