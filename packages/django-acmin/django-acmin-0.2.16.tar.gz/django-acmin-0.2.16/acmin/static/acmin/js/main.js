var getHash = function () {
    var key = '!';
    var hash = window.location.hash.substring(key.length + 1);
    var args = hash.split('&');
    var hashObj = {};
    for (var i = 0; i < args.length; i++) {
        var entity = args[i];
        var parts = entity.split("=");
        if (parts.length === 2) {
            hashObj[parts[0]] = parts[1];
        }
    }
    return hashObj;
};

var activeNode = function (name) {
    if (name.substr(0, 1) === "/") name = name.substr(1);
    var divId = "#" + name.replace(/\//g, "-");
    //alert(divId)
    parts = divId.split("-");//只保留前面1个字段
    if (parts.length > 1) {
        divId = parts[0];
    }
    if (window.activeDiv) {
        var obj = $(activeDiv);
        if (obj) {
            obj.removeClass("active");
        }
    }

    $(divId).addClass("active");
    window.activeDiv = divId;
    if (!name) {
        name = window.lastName;
    } else {
        window.lastName = name;
    }
};
var contentHtml = function (result) {
    if (checkReload(result)) {
        $("#main-content").html(result);
    }
};
var handleError = function (data) {
    console.log(data)
    if (checkReload(data)) {
        var message = "";
        if (data instanceof Object) {
            message += data.responseText + "</br>\n";
        } else {
            message += data
        }
        contentHtml(message);
    }
};
var checkReload = function (result) {
    if (result && result.indexOf && (result.indexOf("reload-page") > 0 || result.indexOf("page-index-page") > 0)) {
        window.location = "/";
        return false;
    }
    return true
};
var doClone = function (name) {
    $.ajax({
        type: "GET", url: window.urlPrefix + name + "/clone",
        success: function (result) {
            checkReload(result);
            history.go(-1);
        },
        error: function (data) {
            handleError(data);
        }
    });
}
var doDelete = function (name) {
    var csrfContainer = $("#csrf-container");
    if (csrfContainer.length === 0) {
        history.go(-1);
        return;
    }
    bootbox.confirm({
        size: "small", title: "确认要删除吗?", message: " ",
        buttons: {
            confirm: {label: '确定', className: 'btn-success'},
            cancel: {label: '取消', className: 'btn-grey'}
        },
        callback: function (result) {
            if (result) {
                $.ajax({
                    type: "GET", url: window.urlPrefix + '/token/', success: function (token) {
                        $.ajax({
                            type: "POST", url: window.urlPrefix + name + "/delete/", data: {'csrfmiddlewaretoken': token},
                            success: function (result) {
                                checkReload(result);
                                history.go(-1);
                            },
                            error: function (data) {
                                handleError(data);
                            }
                        });
                    }
                });
            } else {
                history.go(-1);
            }
        }
    });

};

var checkHash = function () {
    var hash = getHash();
    var name = hash.name;
    if (!name) name = window.defaultNode;
    activeNode(name);
    var action = hash.action;
    if (action === undefined) {
        show(name, hash.params);
    } else if (action === "delete") {
        doDelete(name);
    } else if (action === 'clone') {
        doClone(name)
    }
};

var ajaxSubmit = function (form) {
    var messageLabel = $("#form-save-success");
    messageLabel.hide();
    //var data = $(form).serialize();
    var data = new FormData(form);
    $.ajax({
        processData: false,
        contentType: false, // 注意这里应设为false
        type: "POST", url: window.formAction, data: data,
        success: function (result) {
            contentHtml(result);
        },
        error: function (data) {
            handleError(data);
        }
    });
};

var reloadContent = function () {
    showUrl()
}

var showUrl = function (url) {
    if (!url) url = window.lastUrl;
    $.ajax({
        type: "GET", url: url,
        success: function (result) {
            contentHtml(result);
        },
        error: function (result) {
            handleError(result);
        }
    });
};

var show = function (name, params) {
    contentHtml($("#loading-message").html());
    if (params) {
        name = name + "?" + base64Decode(params);
    }
    var url = window.urlPrefix + name + "";
    window.lastUrl = url;
    showUrl(url);
};

var updateHashParam = function (paramsObj) {
    var parseParams = function (params) {
        var hashObj = {};
        var args = params.split('&');

        for (var i = 0; i < args.length; i++) {
            var entity = args[i];
            var parts = entity.split("=");
            if (parts.length === 2) {
                hashObj[parts[0]] = decodeURI(parts[1]);
            }
        }
        return hashObj;
    };

    var hash = getHash();
    var params = hash.params;
    var obj = {};
    if (params) {
        obj = parseParams(base64Decode(params))
    }
    for (var key in paramsObj) {
        obj[key] = paramsObj[key];
    }
    var hashUrl = "!";
    for (var key in hash) {
        if (key !== "params") hashUrl += key + "=" + hash[key] + "&";
    }
    var paramUrl = "";
    for (var key in obj) {
        paramUrl += key + "=" + encodeURI(obj[key]) + "&"
    }
    hashUrl += "params=" + base64Encode(paramUrl);
    location.hash = hashUrl;
};

var doSearch = function (input) {
    updateHashParam({___fuzzy_search_key__: input.value, page: 1})
};

var sort = function (field) {
    updateHashParam({sort: field})
};
var gotoPage = function (page) {
    updateHashParam({page: page})
};

window.addEventListener("hashchange", function (event) {
    checkHash()
}, false);


var exportExcel = function () {
    var hash = getHash();
    var name = hash.name + "export"
    var params = hash.params

    if (params) {
        name = name + "?" + base64Decode(params);
    }
    url = window.urlPrefix + name + "";
    window.location = url
    //alert(url)
};

var jsonPost = function (url, jsonData, callback) {
    $.ajax({
        type: "GET", url: window.urlPrefix + '/token/', success: function (token) {
            jsonData['csrfmiddlewaretoken'] = token;
            $.ajax({type: "post", url: url, data: jsonData, success: callback});
        }
    });
};


