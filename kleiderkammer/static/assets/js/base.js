"use strict";

Handlebars.registerHelper("format_date", function (dateString, format) {
    return $.format.date(dateString, format);
});
