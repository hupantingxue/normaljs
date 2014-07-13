function setCookie(c_name, value, expireDays){
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expireDays);
    document.cookie = c_name + "=" + escape(value) + ((expireDays==null)? "" : ";expires="+ exdate.toGMTString());
}

function getHHmmss(){
    var date = new Date();
    var hour = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
    var minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
    var second = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
    return '' + hour + minute + second;
}

function getUuid() {
    return (function() {
        var search = window.location.search;
        var arrStr = search.substr(1, search.length).split('&');
        for (var i = 0; i < arrStr.length; i++) {
            var temp = arrStr[i].split('=');
            if (temp[0] == 'code') {
                return unescape(temp[1]);
            }
        }
    })()
}

var sc = sc || {};
var app = app || {};
(function(ex) {
    var dropdown = function(containerId, element) {
        $("#" + containerId).find(element).bind("click", function() {
            if (user_status == "NEW_USER") {
                $(".container").hide();
                var registerView = new app.RegisterView({
                        backTo: "menu-container"
                });
                $(".main-container").append(registerView.render().el)
            } else {
                var isBlock = $("#menu-dropdown").css("display");
                if (isBlock == "block") {
                    $("#menu-dropdown").hide();
                    $("#menu-shadow").hide()
                } else {
                    $("#menu-dropdown").show();
                    $("#menu-shadow").show()
                }
            }
            if (user_status == "CUSTOMER" && !sc.getWechatId()) {
                $("#logout > a").text("登录")
            } else {
                $("#logout > a").text("退出登录")
            }
        })
    };
    ex.dropdown = dropdown
})(sc);

// toggle tabs dropdown
sc.toggleTypesDropdown = function() {
    var dropdown = $('#types-dropdown');
    if (dropdown.css('display') === 'none') {
        dropdown.css('display', 'block');
        var height = (parseInt(dropdown.css('height')) * 2 + 27) + 'px';
        $('#mainList').css('margin-top', height);
    } else {
        dropdown.css('display', 'none').css('margin-top','0px');
        $('#mainList').css('margin-top','0px');
    }
};

(function(ex) {
    var normalizeNumber = function(number) {
        if (number < 10) {
            number = '0' + number
        }
        return number
    };
    ex.normalizeNumber = normalizeNumber
})(sc);

(function(ex) {
    var togglePic = function(element) {
        $(element).bind('click', function() {
            setCookie("pic_status", "no", 100);
            window.location.reload()
        })
    };
    ex.togglePic = togglePic
})(sc);

(function(ex) {
    var getWechatId = function() {
        var arrStr = document.cookie.split("; ");
        for (var i = 0; i < arrStr.length; i++) {
            var temp = arrStr[i].split("=");
            if (temp[0] == 'wechat_id') return unescape(temp[1])
        }
    };
    ex.getWechatId = getWechatId
})(sc);

$(function() {
//    document.onclick = function(e) {
//            e.preventDefault()
//    }
    app.menuView = new app.MenuView();
    app.menuView.setPic(true);
    app.shoppingCart = new app.Order();
    app.vegetableCollection = new app.ItemCollection();
    app.meatCollection = new app.ItemCollection();
    app.soupCollection = new app.ItemCollection();
    app.specialityCollection = new app.ItemCollection();
    app.shoppingCartV = new app.ShoppingCartView({
        model: app.shoppingCart
    });
    $("#menu-container").append(app.shoppingCartV.render().el);
    $('.loader-mask').remove();
    app.menuView.renderList(catalogs[slctidx].Catalog.id);
    $('.backToTop').click(function() {
        $(window).scrollTop(2)
    });
    $("#menu-shadow").bind("click", function() {
        $("#menu-dropdown").hide();
        $("#menu-shadow").hide()
    });
    $("#todayList").bind('click', function() {
        window.location.reload()
    });
    $("#myOrder").bind('click', function() {
        $(".container").css('display', 'none');
        if (user_status == "CUSTOMER" && !sc.getWechatId()) {
            $("#menu-shadow").click();
            $(".container").hide();
            var loginView = new app.LoginView({
                    backTo: "menu-container"
            });
            $(".main-container").append(loginView.render().el)
        } else if ($("#myOrders-container").length > 0) {
            $("#myOrders-container").show()
        } else {
            app.myOrderView = new app.MyOrdersView()
        }
        $("#menu-shadow").click()
    });
    $("#logout").click(function() {
        if (user_status == "CUSTOMER" && !sc.getWechatId()) {
            $("#menu-shadow").click();
            $(".container").hide();
            var loginView = new app.LoginView({
                    backTo: "menu-container"
            });
            $(".main-container").append(loginView.render().el)
        } else {
            setCookie("wechat_id", "", -1);
            var popup = new app.OrderInfoPopupView({
                msg: "退出登录成功！"
            });
            $("#menu-dropdown").append(popup.render().el);
            setTimeout(function() {
                $("#menu-shadow").click();
                $(".container").hide();
                var loginView = new app.LoginView({
                    backTo: "menu-container"
                });
                $(".main-container").append(loginView.render().el)
            }, 2000)
        }
    });
//    $("#home-header").bind("touchmove", {}, function(e) {
//        e.preventDefault();
//    });
    $(window).scrollTop(2)
});
