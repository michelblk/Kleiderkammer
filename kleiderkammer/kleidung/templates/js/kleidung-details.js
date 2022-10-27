$(function () {
    $(document).on('click', '.waschen-button', function (e) {
        e.preventDefault();
        const kleidung_id = $("#kleidung-details").data('id');
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