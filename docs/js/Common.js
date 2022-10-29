/*
 * @Author: LetMeFly
 * @Date: 2022-10-29 09:59:22
 * @LastEditors: LetMeFly
 * @LastEditTime: 2022-10-29 13:50:10
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

function getUserInfo() {
    var info = {"login": false};
    $.get(
        "https://back.share1024.letmefly.xyz/user/baseInfo/",
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
    });
}