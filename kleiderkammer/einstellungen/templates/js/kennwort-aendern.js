'use strict';

$(function () {
    $("#kennwort-aendern").submit(function (e) { // FIXME submit funktioniert nicht
        e.preventDefault();

        $.ajax({
            cache: false,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: $("#kennwort-aendern").serialize(),
            method: 'POST',
            success: function () {
                alert("Kennwort geändert");
            },
            url: "{{ url_for('einstellungen_api.change_password') }}"
        });
    });
});