var showDateTimePicker = function (jqueryElement, format) {
    if (!jqueryElement || !jqueryElement.length) return;
    jqueryElement.datetimepicker({
        format: format,//'YYYY-MM-DD HH:mm:ss',//use this option to display seconds
        icons: {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down',
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-arrows ',
            clear: 'fa fa-trash',
            close: 'fa fa-times'
        }
    }).next().on(ace.click_event, function () {
        $(this).prev().focus();
    });
};

var clearOptions = function (targetId) {
    $(targetId + " option").remove();
    $(targetId).append("<option value=''>---------</option>");
};
var updateOptions = function (result, selectId) {
    $(result).each(function (i, obj) {
        var text = obj["title"];
        if (!text) text = obj['name'];
        var option = "<option value='" + obj.id + "'>" + text + "</option>";
        $(selectId).append(option);
    })
};

