function partialUpdate(class_name, id, element, isCheckbox) {
    let url = window.urlPrefix + "/" + class_name + "/" + id + "/";
    let value = isCheckbox ? element.checked : element.value;
    $.getJSON(url, {attribute: element.name, value: value, partial: true}, function (result) {
        console.log(result)
        reloadContent();
    });
}



