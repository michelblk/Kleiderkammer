'use strict';

$(function () {
    $("#form").submit(function (event) {
        event.preventDefault();

        $.ajax({
            cache: false,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: $("#form").serialize(),
            method: 'POST',
            success: function () {
                location.href = "{{ url_for('mitglieder.index') }}";
            },
            url: "{{ url_for('mitglieder_api.hinzufuegen') }}"
        });
    });
});