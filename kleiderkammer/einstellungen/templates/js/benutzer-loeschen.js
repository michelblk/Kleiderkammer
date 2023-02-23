"use strict";

$(function () {
    $("#benutzer-loeschen").submit(function (e) {
        e.preventDefault();

        $.ajax({
            cache: false,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            method: "DELETE",
            success: function () {
                location.href = "{{ url_for('index') }}";
            },
            url: "{{ url_for('einstellungen_api.remove_user', userid=current_user.id) }}",
        });
    });
});
