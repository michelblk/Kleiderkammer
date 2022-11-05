'use strict';

$(function () {
    $(document).on('shown.bs.modal', '#kleidung-details', function (e) {
        const mitgliedId = $("#kleidung-details .modal").data("kleidung-id");

        requestAktuellenStatus(mitgliedId, updateKleidungsstatus, () => {
            alert("Kleidungsinformationen konnten nicht abgerufen werden.");
        });
    });


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
                location.href = "{{ url_for('kleidung.index') }}";
            },
            url: "{{ url_for('kleidung_api.toggle_waesche') }}"
        });
    });
});

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