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
    const kleidungId = $("#kleidung-details .modal").data("kleidung-id");

    requestAktuellenStatus(kleidungId, updateKleidungsstatus, () => {
        alert("Kleidungsinformationen konnten nicht abgerufen werden.");
    });

    requestHistory(kleidungId, updateHistory, () => {
        alert("Kleidungshistorie konnte nicht abgerufen werden");
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

function requestHistory(kleidungId, success, failure) {
    var data = {"leihen": [], "waeschen": []};
    $.when(
        $.ajax({
            cache: false,
            method: 'GET',
            success: function (leihen) {
                data["leihen"] = leihen;
            },
            failure: failure,
            url: "{{ url_for('kleidung_api.leihen', kleidung_id='_kleidung_id_') }}".replace("_kleidung_id_", kleidungId)
        }),
        $.ajax({
            cache: false,
            method: 'GET',
            success: function (waeschen) {
                data["waeschen"] = waeschen;
            },
            failure: failure,
            url: "{{ url_for('kleidung_api.waeschen', kleidung_id='_kleidung_id_') }}".replace("_kleidung_id_", kleidungId)
        })
    ).then(function () {
        const merged_data = [];

        $.each(data["leihen"], function (i, item) {
            merged_data.push({
                "von": item.von,
                "bis": item.bis,
                "aktion": "Leihe",
                "mitglied": {
                    "vorname": item.mitglied.vorname,
                    "nachname": item.mitglied.nachname
                }
            });
        });
        $.each(data["waeschen"], function (i, item) {
            merged_data.push({
                "von": item.von,
                "bis": item.bis,
                "aktion": "Wäsche",
                "mitglied": undefined
            });
        });

        merged_data.sort((a, b) => {
            if (a.bis && b.bis) {
                return Date.parse(b.bis) - Date.parse(a.bis)
            }
            if (!a.bis && b.bis) {
                return -1;
            }
            if (a.bis && !b.bis) {
                return 1;
            }
            return Date.parse(b.von) - Date.parse(a.von)
        });

        console.log(merged_data);

        success(merged_data);
    });
}

function updateHistory(data) {
    const historyTemplateObj = $("#kleidung-history-template");
    const historyTemplate = Handlebars.compile(historyTemplateObj.html());
    const history = $("#kleidung-history");

    history.html(historyTemplate(data));
}