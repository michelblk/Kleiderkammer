'use strict';

$(function () {
    $("#modell").change(function () {
        var input = $("#modell")[0];
        var datalist = $("#modelle")[0];
        var selectedOption = datalist.querySelector(`[value="${input.value}"]`);

        if (selectedOption) {
            const hersteller = $(selectedOption).data('hersteller');
            const kategorie = $(selectedOption).data('kategorie');
            $("#hersteller").val(hersteller);
            $("#kategorie").val(kategorie);
        }
    });

    // on submit
    $("#form").submit(function (event) {
        event.preventDefault();

        $.ajax({
            cache: false,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: $("#form").serialize(),
            method: 'POST',
            success: function () {
                location.href = "{{ url_for('kleidung.index') }}";
            },
            url: "{{ url_for('kleidung_api.hinzufuegen') }}"
        });
    });
});