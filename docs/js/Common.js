/*
 * @Author: LetMeFly
 * @Date: 2022-10-29 09:59:22
 * @LastEditors: LetMeFly
 * @LastEditTime: 2022-10-29 19:47:40
 */
function adjust() {
    // adjustFooter
    const height = $("#footer").height();
    $("#beforeFooter").height(height);
}

function parseUrlParm() {  // 仅支持一个?
    const url = new URL(location.href);
    const params = new URLSearchParams(url.search);
    const data = Object.fromEntries(params);
    return data;
}

function setCookie(cname, cvalue) {
    // 此函数参考自[菜鸟教程](https://www.runoob.com/js/js-cookies.html)
    document.cookie = cname + "=" + cvalue + "; expires=Mon, 05 Oct 2122 11:05:52 GMT; path=/";
}

function getCookie(cname) {
    // 此函数参考自[菜鸟教程](https://www.runoob.com/js/js-cookies.html)
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function getUserInfo() {
    var info = {"login": false};
    if (!getCookie("warrant1024")) {
        return info;
    }
    $.post(
        "https://back.share1024.letmefly.xyz/user/baseInfo/",
        {
            "warrant1024": getCookie("warrant1024")
        },
        function(response, status) {
            if (status == "success") {
                info = response;
            }
            else {
                console.log(status);
            }
        },
    ).fail(
        function() {
            alert(" 获取用户信息失败 ", hei=60, time=2500);
        }
    ).then(function() {
        if ($("#User")) {
            if (info.username) {
                $("#User").children("#User_Text").text(info.username);
                $("#User").children("#User_Text").attr("href", "User.html");
            }
            if (info.cardNotShare) {
                alert(" 有领取的卡牌未传递哦 ", height=60, time=2000);
                setTimeout(() => {
                    const nowHref = location.href;
                    if (nowHref.indexOf("/card1.html") == -1 || parseUrlParm().cardID != info.cardNotShare) {
                        // TODO: TEST
                        location.href = "card1.html?cardID=" + info.cardNotShare;
                    }
                }, 1000);
            }
        }
        return info;
    });
}