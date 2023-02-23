"use strict";

$(function () {
    $("#benutzer-erstellen").submit(function (e) {
        e.preventDefault();

        $.ajax({
            cache: false,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            data: $("#benutzer-erstellen").serialize(),
            method: "PUT",
            success: function () {
                alert("Benutzer angelegt");
            },
            url: "{{ url_for('einstellungen_api.add_user') }}",
        });
    });
});
