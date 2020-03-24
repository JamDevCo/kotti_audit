/* JS */

window.datepicker = {
    toDisplay: function (date, format, language) {
        var d = new Date(date);
        d.setDate(d.getDate() - 7);
        return d.toISOString();
    },
    toValue: function (date, format, language) {
        var d = new Date(date);
        d.setDate(d.getDate() + 7);
        return new Date(d);
    }
};