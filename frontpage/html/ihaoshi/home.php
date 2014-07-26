<!DOCTYPE html>
<!-- saved from url=(0122)http://www.ihaoshi.cn/ihaoshi/home.php -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="./files/reset.css" media="all">
<link rel="stylesheet" type="text/css" href="./files/common.css" media="all">
<link rel="stylesheet" type="text/css" href="./files/font-awesome.css" media="all">
<link rel="stylesheet" type="text/css" href="./files/home-62.css" media="all">
<link rel="stylesheet" type="text/css" href="./files/home-menu-3.css" media="all">
<script type="text/javascript" async="" src="./files/wtj.js"></script><script type="text/javascript" src="./files/maivl.js"></script><style type="text/css"></style>
<script type="text/javascript" src="./files/jQuery.js"></script>
<script type="text/javascript" src="./files/zepto.js"></script>
<script type="text/javascript" src="./files/swipe.js"></script>
<title>爱好食</title>
        <meta content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport">
        <meta name="Keywords" content="爱好食、简单客、微信定制开发、微信托管、微网站、微商城、微营销">
        <meta name="Description" content="简单客，国内最大的微信公众智能服务平台，八大微体系：微菜单、微官网、微会员、微活动、微商城、微推送、微服务、微统计，企业微营销必备。">
        <!-- Mobile Devices Support @begin -->
            
            <meta content="no-cache,must-revalidate" http-equiv="Cache-Control">
            <meta content="no-cache" http-equiv="pragma">
            <meta content="0" http-equiv="expires">
            <meta content="telephone=no, address=no" name="format-detection">
            <meta name="apple-mobile-web-app-capable" content="yes"> <!-- apple devices fullscreen -->
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <!-- Mobile Devices Support @end -->
        <link rel="shortcut icon" href="./files/favicon.ico">
    </head>
    <body onselectstart="return true;" ondragstart="return false;">
            

<div class="body">
    <section>
            <!--
    幻灯片管理
    -->
    <div style="-webkit-transform:translate3d(0,0,0);">
        <div id="banner_box" class="box_swipe" style="visibility: visible;">
            <ul style="list-style: none; width: 5760px; transition: 0ms; -webkit-transition: 0ms; -webkit-transform: translate3d(-4480px, 0, 0);">
                <li style="width: 640px; display: table-cell; vertical-align: top;">
                <a href="#">
                    <img src="./files/111.jpg" alt="1" style="width:100%;">
                </a>
                </li>
                <li style="width: 640px; display: table-cell; vertical-align: top;">
                <a href="#">
                    <img src="./files/20131105222730_70527.jpg" alt="1" style="width:100%;">
                </a>
                </li>
               </ul>
           <ol>
              <li class=""></li>
              <li class=""></li>
              <li class=""></li>
              <li class=""></li>
              <li class=""></li>
              <li class=""></li>
              <li class=""></li>
              <li class="on"></li>
              <li class=""></li>
          </ol>
        </div>
    </div>
        <script>
        $(function(){
            new Swipe(document.getElementById('banner_box'), {
                speed:500,
                auto:3000,
                callback: function(){
                    var lis = $(this.element).next("ol").children();
                    lis.removeClass("on").eq(this.index).addClass("on");
                }
            });
        });
    </script>
<header>
    </header> 
<div>
  <ul id="list_ul" class="list_ul">
    <li class="box">

    <dl>
    <a href="http://www.ihaoshi.cn:8600/microfront/?code=<?php echo $_GET["code"]?>&idx=0">
      <dd>
       <div>
           <span></span>
       </div>
         </dd>
    <dt>绿色蔬菜</dt>
    </a>
    </dl>

    <dl>
    <a href="http://www.ihaoshi.cn:8600/microfront/?code=<?php echo $_GET["code"]?>&idx=1">
      <dd>
      <div>
        <span></span>
      </div>
      </dd>
        <dt>好食有机</dt>
    </a>
    </dl>

    <dl>
    <a href="http://www.ihaoshi.cn:8600/microfront/?code=<?php echo $_GET["code"]?>&idx=2">
       <dd>
           <div>
                <span></span>
           </div>
       </dd>
       <dt>好食海鲜</dt>
        </a>
    </dl>
    </li>

<li>
   <dl>
    <a href="http://wx.wsq.qq.com/259096143">
      <dd>
       <div>
           <span></span>
       </div>
         </dd>
    <dt>互动社区</dt>
    </a>
    </dl>
</li>
            </ul>
        </div>

        <!--div style="align:center" class="logo">
 
          <span>                                             </span>
          <img src="./files/ihs.jpg" alt="爱好食" height="18">
          <span style="color:#070;font-size:12px;text-align:center;">打造简单、健康、时尚的都市生活</span>
        </div-->
    </section>
</div>
<!--
导航菜单
   后台设置的快捷菜单
-->

<!--
分享前控制
-->
    <script type="text/javascript">
        
        window.shareData = {
            "imgUrl": "http://www.ihaoshi.cn/ihaoshi/files/ihs.jpg",
            "timeLineLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&wxref=mp.weixin.qq.com",
            "sendFriendLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&wxref=mp.weixin.qq.com",
            "weiboLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&wxref=mp.weixin.qq.com",
            "tTitle": "欢迎光临爱好食微信平台",
            "tContent": "好食来，福利到，你选菜，我买单啦！",
            "fTitle": "欢迎光临爱好食微信平台",
            "fContent": "好食来，福利到，你选菜，我买单啦！",
            "wContent": "好食来，福利到，你选菜，我买单啦！"
        };
            </script>
                    <footer style="overflow:visible;">
        <div style="align:center;color:#fff;font-size:12px;text-align:center;" class="logo">
 
          <span>                                             </span>
          <img src="./files/ihs.jpg" alt="爱好食" height="16">
          <span style="color:#070;font-size:12px;text-align:center;">打造简单、健康、时尚的都市生活</span>
        </div>
                </div>
            </footer>
                <!--div mark="stat_code" style="width:0px; height:0px; display:none;">
                    </div-->
    
        <script type="text/javascript">
/**
 * 默认分享出去的数据
 *
 */
function getShareImageUrl(){
    var share_imgurl = "";
    if("" == share_imgurl){
        var shareImgObj = document.getElementsByClassName("shareImgUrl")[0];
        if('undefined' != typeof(shareImgObj)){
            share_imgurl = shareImgObj.src;
        }
    }
    return window.shareData.imgUrl || share_imgurl;
}

window.shareData = window.shareData || {
    "timeLineLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&from=1&wxref=mp.weixin.qq.com",
    "sendFriendLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&from=1&wxref=mp.weixin.qq.com",
    "weiboLink": "http://www.ihaoshi.cn/ihaoshi/home.php?code=fromUsername&from=1&wxref=mp.weixin.qq.com",
    "tTitle": document.title,
    "tContent": document.title,
    "fTitle": document.title,
    "fContent": document.title,
    "wContent": document.title
}
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
    // 发送给好友
    WeixinJSBridge.on('menu:share:appmessage', function (argv) {
        WeixinJSBridge.invoke('sendAppMessage', { 
            "img_url": getShareImageUrl(),
            "img_width": "640",
            "img_height": "640",
            "link": window.shareData.sendFriendLink,
            "desc": window.shareData.fContent,
            "title": window.shareData.fTitle
        }, function (res) {
            weimobAfterShare("owK7EjiSDgRfpA6BIzpNb0zcn52k",window.shareData.sendFriendLink,'appmessage');
            _report('send_msg', res.err_msg);
        })
    });

    // 分享到朋友圈
    WeixinJSBridge.on('menu:share:timeline', function (argv) {
        WeixinJSBridge.invoke('shareTimeline', {
            "img_url": getShareImageUrl(),
            "img_width": "640",
            "img_height": "640",
            "link": window.shareData.timeLineLink,
            "desc": window.shareData.tContent,
            "title": window.shareData.tTitle
        }, function (res) {
            weimobAfterShare("owK7EjiSDgRfpA6BIzpNb0zcn52k",window.shareData.timeLineLink,'timeline');
            _report('timeline', res.err_msg);
        });
    });

    // 分享到微博
    WeixinJSBridge.on('menu:share:weibo', function (argv) {
        WeixinJSBridge.invoke('shareWeibo', {
            "content": window.shareData.wContent,
            "url": window.shareData.weiboLink
        }, function (res) {
            weimobAfterShare("owK7EjiSDgRfpA6BIzpNb0zcn52k",window.shareData.weiboLink,'weibo');
            _report('weibo', res.err_msg);
        });
    });
}, false);
</script><script src="./files/h.js" type="text/javascript"></script>
<script type="text/javascript" src="./files/ChatFloat.js"></script>
<script type="text/javascript">
var str_domain = location.href.split('/',4)[2];
var boolIsTest = true;
if(str_domain == 'www.ihaoshi.cn' || str_domain.indexOf('www.ihaoshi.cn') > 0){
    boolIsTest = false;
}
new ChatFloat({
        AId: '14924',
        openid: "owK7EjiSDgRfpA6BIzpNb0zcn52k",
        top:150,
        right:0,
        IsTest:boolIsTest
});
</script>


</body></html>
