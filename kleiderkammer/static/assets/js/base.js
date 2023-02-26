"use strict";

Handlebars.registerHelper("format_date", function (dateString, format) {
    if (dateString && format) {
        return $.format.date(dateString, format);
    }
    return undefined;
});
