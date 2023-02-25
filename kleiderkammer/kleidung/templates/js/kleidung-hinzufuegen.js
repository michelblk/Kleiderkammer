"use strict";

$(function () {
    $("#modell").bind("input", function () {
        var input = $("#modell");
        var datalist = $("#modelle")[0];
        var selectedOption = datalist.querySelector(`[value="${input.val()}"]`);

        if (selectedOption) {
            const hersteller = $(selectedOption).data("hersteller");
            const kategorie = $(selectedOption).data("kategorie");
            const modell = $(selectedOption).data("modell");
            input.val(modell); // überschreibe input-Wert, da Option option-index einsetzt
            $("#hersteller").val(hersteller);
            $("#kategorie").val(kategorie);
            $("#code").focus();
        }
    });

    // on submit
    $("#form").submit(function (event) {
        event.preventDefault();

        $.ajax({
            cache: false,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            data: $("#form").serialize(),
            method: "POST",
            success: function () {
                location.href = "{{ url_for('kleidung.index') }}";
            },
            url: "{{ url_for('kleidung_api.hinzufuegen') }}",
        });
    });
});
