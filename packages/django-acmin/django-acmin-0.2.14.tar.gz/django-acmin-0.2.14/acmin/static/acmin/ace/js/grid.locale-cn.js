!
    function (a) {
        "use strict";
        "function" == typeof define && define.amd ? define(["jquery", "../grid.base"], a) : a(jQuery)
    }(function (a) {
        a.jgrid = a.jgrid || {},
        a.jgrid.hasOwnProperty("regional") || (a.jgrid.regional = []),
            a.jgrid.regional.en = {
                defaults: {
                    recordtext: "正在浏览{0}-{1},共{2}",
                    emptyrecords: "没有数据",
                    loadtext: "载入中...",
                    savetext: "正在保存...",
                    pgtext: "第 {0} 页 {1}",
                    pgfirst: "第一页",
                    pglast: "最后一页",
                    pgnext: "下一页",
                    pgprev: "上一页",
                    pgrecs: "Records per Page",
                    showhide: "Toggle Expand Collapse Grid",
                    pagerCaption: "Grid::Page Settings",
                    pageText: "Page:",
                    recordPage: "Records per Page",
                    nomorerecs: "No more records...",
                    scrollPullup: "Pull up to load more...",
                    scrollPulldown: "Pull down to refresh...",
                    scrollRefresh: "Release to refresh..."
                },
                search: {
                    caption: "查找记录...",
                    Find: "查找",
                    Reset: "重置",
                    odata: [{
                        oper: "eq",
                        text: "等于"
                    },
                        {
                            oper: "ne",
                            text: "不等于"
                        },
                        {
                            oper: "lt",
                            text: "小于"
                        },
                        {
                            oper: "le",
                            text: "小于等于"
                        },
                        {
                            oper: "gt",
                            text: "大于"
                        },
                        {
                            oper: "ge",
                            text: "大于等于"
                        },
                        {
                            oper: "bw",
                            text: "开始于"
                        },
                        {
                            oper: "bn",
                            text: "不开始于"
                        },
                        {
                            oper: "in",
                            text: "包含"
                        },
                        {
                            oper: "ni",
                            text: "不包含"
                        },
                        {
                            oper: "ew",
                            text: "结束于"
                        },
                        {
                            oper: "en",
                            text: "不结束于"
                        },
                        {
                            oper: "cn",
                            text: "包含"
                        },
                        {
                            oper: "nc",
                            text: "不结束于"
                        },
                        {
                            oper: "nu",
                            text: "为空"
                        },
                        {
                            oper: "nn",
                            text: "不为空"
                        }],
                    groupOps: [{
                        op: "AND",
                        text: "所有"
                    },
                        {
                            op: "OR",
                            text: "任一"
                        }],
                    operandTitle: "Click to select search operation.",
                    resetTitle: "Reset Search Value"
                },
                edit: {
                    addCaption: "增加",
                    editCaption: "编辑",
                    bSubmit: "确定",
                    bCancel: "取消",
                    bClose: "关闭",
                    saveData: "Data has been changed! Save changes?",
                    bYes: "是",
                    bNo: "否",
                    bExit: "取消",
                    msg: {
                        required: "必填项",
                        number: "请输入有效数字",
                        minValue: "value must be greater than or equal to ",
                        maxValue: "value must be less than or equal to",
                        email: "不是有效邮箱地址is not a valid e-mail",
                        integer: "请输入有效数字",
                        date: "请输入有效日期",
                        url: "不是一个有效链接，链接必须以'http://'或者'https://'开头",
                        nodefined: " is not defined!",
                        novalue: " return value is required!",
                        customarray: "Custom function should return array!",
                        customfcheck: "Custom function should be present in case of custom checking!"
                    }
                },
                view: {
                    caption: "查看",
                    bClose: "关闭"
                },
                del: {
                    caption: "删除",
                    msg: "确定要删除吗?",
                    bSubmit: "删除",
                    bCancel: "取消"
                },
                nav: {
                    edittext: "",
                    edittitle: "编辑所选",
                    addtext: "",
                    addtitle: "添加",
                    deltext: "",
                    deltitle: "删除所选",
                    searchtext: "",
                    searchtitle: "查找",
                    refreshtext: "",
                    refreshtitle: "刷新",
                    alertcap: "警告",
                    alerttext: "请先选择",
                    viewtext: "",
                    viewtitle: "查看所选",
                    savetext: "",
                    savetitle: "保存",
                    canceltext: "",
                    canceltitle: "取消编辑",
                    selectcaption: "Actions..."
                },
                col: {
                    caption: "选择列",
                    bSubmit: "确定",
                    bCancel: "取消"
                },
                errors: {
                    errcap: "错误",
                    nourl: "No url is set",
                    norecords: "No records to process",
                    model: "Length of colNames <> colModel!"
                },
                formatter: {
                    integer: {
                        thousandsSeparator: ",",
                        defaultValue: "0"
                    },
                    number: {
                        decimalSeparator: ".",
                        thousandsSeparator: ",",
                        decimalPlaces: 2,
                        defaultValue: "0.00"
                    },
                    currency: {
                        decimalSeparator: ".",
                        thousandsSeparator: ",",
                        decimalPlaces: 2,
                        prefix: "",
                        suffix: "",
                        defaultValue: "0.00"
                    },
                    date: {
                        dayNames: ["Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                        AmPm: ["am", "pm", "AM", "PM"],
                        S: function (a) {
                            return 11 > a || a > 13 ? ["st", "nd", "rd", "th"][Math.min((a - 1) % 10, 3)] : "th"
                        },
                        srcformat: "Y-m-d",
                        newformat: "n/j/Y",
                        parseRe: /[#%\\\/:_;.,\t\s-]/,
                        masks: {
                            ISO8601Long: "Y-m-d H:i:s",
                            ISO8601Short: "Y-m-d",
                            ShortDate: "n/j/Y",
                            LongDate: "l, F d, Y",
                            FullDateTime: "l, F d, Y g:i:s A",
                            MonthDay: "F d",
                            ShortTime: "g:i A",
                            LongTime: "g:i:s A",
                            SortableDateTime: "Y-m-d\\TH:i:s",
                            UniversalSortableDateTime: "Y-m-d H:i:sO",
                            YearMonth: "F, Y"
                        },
                        reformatAfterEdit: !1,
                        userLocalTime: !1
                    },
                    baseLinkUrl: "",
                    showAction: "",
                    target: "",
                    checkbox: {
                        disabled: !0
                    },
                    idName: "id"
                }
            }
    });