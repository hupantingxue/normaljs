<html>
	<head>
	  <meta http-equiv="Content-type" content="text/html; charset=utf-8">
	  <meta name="viewport" content="	width=100%; initial-scale=1; maximum-scale=1; minimum-scale=1; user-scalable=no;">
	  <meta name="apple-mobile-web-app-capable" content="yes">
	  <title>爱好食</title>
	  <link rel="stylesheet" href="css/style.css?5">		
    <style type="text/css"></style><style type="text/css"></style><script>window["_GOOG_TRANS_EXT_VER"] = "1";</script>
  </head>

<body>
	<div class="main-container">
	   <div id="myOrders-container" class="container">
       <div class="my-order-header">
           <span>我的订单</span>
           <div class="dotted-divider"></div>
       </div> 
       <?php 
           $openid = $_GET["code"]; 
           //echo $openid;
           $orderfn = "/home/otto/src/github/normaljs/microfront/orders/" . $openid . "/0.json";
           $orderhis_fn = "/home/otto/src/github/normaljs/microfront/orders/" . $openid . "/1.json";
           $order_json = "";
           $orderhis_json = "";
           if (file_exists($orderfn) && is_readable ($orderfn)) {
               $order_json = file_get_contents($orderfn);
           }
           if (file_exists($orderhis_fn) && is_readable ($orderhis_fn)) {
               $orderhis_json = file_get_contents($orderhis_fn);
           }
           $order_obj = json_decode($order_json);
           $tmp = $order_obj->rt_obj->data;
           if (isset($tmp)) {
           // 每个历史订单
           foreach ($tmp->orders as $unit) {
               // every order info
               $order_id = $unit->Order->id;
               $order_str = '<div class="myOrderList"><div><div class="orderResult-form"><div><div class="orderResult-list" id="items-order-result"><div class="order-info"><span>订单号：<span id="order-no">'.$order_id.'</span></span><span class="date" style="float: right"></span></div><div class="order-list" id="item-order-list">';
               echo $order_str;
               $order_info = $tmp->orderItems->$order_id;
               // 每个订单所有的菜品
               echo "<ul>";
               foreach ($order_info as $item) {
                   // every order item in order info
                   $price = $item->OrderGoods->goods_price;
                   $total_price = sprintf("%.2f", $price * $item->OrderGoods->goods_num);
                   echo '<li><span class="order-item-name"></span><span class="order-item-name">'.$item->OrderGoods->goods_name.'</span><span class="order-item-price">￥'.$total_price.'</span><span class="order-item-amount">'.$item->OrderGoods->goods_num.'份</span></li>';
               }
               echo "</ul>";
               echo '</div><div class="divider"></div><div class="total-info"><span>运费：<span>0.00</span>元，共<span>'.$unit->Order->order_money.'</span>元</div></div></div></div></div></div>';
           }
           }  // if isset

           $order_obj = json_decode($orderhis_json);
           $tmp = $order_obj->rt_obj->data;
           if (isset($tmp)) {
           // 每个订单
           foreach ($tmp->orders as $unit) {
               // every order info
               $order_id = $unit->Order->id;
               $order_str = '<div class="myOrderList"><div><div class="orderResult-form"><div><div class="orderResult-list" id="items-order-result"><div class="order-info"><span>订单号：<span id="order-no">'.$order_id.'</span></span><span class="date" style="float: right"></span></div><div class="order-list" id="item-order-list">';
               echo $order_str;
               $order_info = $tmp->orderItems->$order_id;
               // 每个订单所有的菜品
               echo "<ul>";
               foreach ($order_info as $item) {
                   // every order item in order info
                   $price = $item->OrderGoods->goods_price;
                   $total_price = sprintf("%.2f", $price * $item->OrderGoods->goods_num);
                   echo '<li><span class="order-item-name"></span><span class="order-item-name">'.$item->OrderGoods->goods_name.'</span><span class="order-item-price">￥'.$total_price.'</span><span class="order-item-amount">'.$item->OrderGoods->goods_num.'份</span></li>';
               }
               echo "</ul>";
               echo '</div><div class="divider"></div><div class="total-info"><span>运费：<span>0.00</span>元，共<span>'.$unit->Order->order_money.'</span>元</div></div></div></div></div></div>';
           } // foreach
           } // if isset

       ?>           
       <!--div class="myOrderList">
       	<div>
           <div class="orderResult-form">
           	  <div>		
                 <div class="order-header">
                     <span class="order-status">状态：<span class="status">20140712 处理中</span></span>
                 </div>
                 <div class="orderResult-list" id="items-order-result">
                     <div class="order-info">
                         <span>
                             订单号：<span id="order-no">201407120234</span>
                         </span>
                         <span class="date" style="float: right"></span>
                     </div> <?php // do nothing;?>
                     <div class="order-list" id="item-order-list">
                         <ul><li>
                             <span class="order-item-name"></span>
                             <span class="order-item-name">有机白萝卜 500g</span>
                             <span class="order-item-price">￥56.00</span>
                             <span class="order-item-amount">2份</span>
	                       </li></ul>
                     </div>
                     <div class="divider"></div>
                     <div class="total-info">
                         <span>
                             运费：<span>0.00</span>元，共<span>56.00</span>元
                         </span>
                     </div>				
                 </div>
	            </div>
	         </div>
	      </div>
	     </div-->
	   </div>
	</div>
	<div id="menu-shadow" hidefocus="true" style="display: none;"></div>
	<div id="menu-dropdown" style="display: none;">
        <div id="menu-arrow"></div>
        <ul>
            <li id="myOrder">
                <a href="javascript:void(0);">我的订单</a>
            </li>
        </ul>
    </div>



	<!-- 弹出窗口模版 -->
	<script type="text/template" id="popupView-template">

	</script>

	<!-- 登录页面模版 -->
	<script type="text/template" id="loginView-template">
		<div class="login-header">
			<!--img class="logo" src="img/logo.png" alt="logo"-->
                        <center><h3>爱好食</h3></center>
			<span class="login-tips">为了您的帐号安全请登陆</span>
		</div>

		<div class="login-form">
			<div class="line">
				<label for="password">姓名：</label>
				<input type="text" name="password" placeholder="">
			</div>
                        <div class="line">
				<label for="account" >手机号：</label>
				<input type="tel" name="account" placeholder="">
			</div>
			<!--a id="forget">忘记密码？</a-->
                        <table style="width:100%;">
                            <tr>
                                <td><button id="login" class="mybtn" style="width:100%;">登 录</button></td>
                                <td><button class="mybtn back" style="width:100%;">返 回</button></td>
                            </tr>
                        </table>
		</div>
	</script>



	<!-- 订单条目视图模版 -->
	<script type="text/template" id="orderItemView-template">
            <div class="confirmation-item">
                <div class="item-info">
                    <span class="item-name" title="<%= Goods.name %>"><%= Goods.name %><br/></span>
                    <span class="item-price-info">
                        <span>
                            <span class="item-total-price">￥<%= parseFloat(total).toFixed(2) %></span>
                            (<span class="item-single-price"><%= parseFloat(Goods.price).toFixed(2) %></span>×<span class="item-amount"><%= count %></span>)
                        </span>
                    </span>
                </div>
                <div class="select-box">
                    <span class="minus disabled">—</span>
                    <input class="amount" type="text" name="amount" value="<%= count %>" autocomplete="off" readonly>
                    <span class="add">+</span>
                </div>
                <div class="delete">
                    <a class="delete-btn" href="javascript:void(0);"><img src="img/delete.png"></a>
                </div>
            </div>
            <div class="divider"></div>
	</script>

	
	<!-- 我的订单视图模版 -->
	<script type="text/template" id="myOrdersView-template">
            <div class="my-order-header">
                <span>我的订单</span>
                <div class="dotted-divider"></div>
            </div>
            
            <div class='myOrderList'></div>
            
            <div class="history-loader">
                <img src="img/timer.png">
                <span>点击查看历史订单</span>
            </div>

            <div class="toolbar">
                <a class="next mybtn" href="javascript:void(0);">
                    <span style="display: block; height: 39px; font-size: 1.2em;">我要订购</span>
                </a>
                <a class="user" href="javascript:void(0);"><img src="img/user.png"></a>
            </div>
	</script>

	<script type="text/template" id="oneDayOrderView-template">
            <div class="orderResult-form"></div>
	</script>

	<!-- 我的订单中普通菜品列表的视图模版 -->
	<script type="text/template" id="itemOrderView-template">		
            <div class="order-header">
                <span class="order-status">状态：<span class="status"><%= order_status %></span></span>
                <% if(can_cancel){ %>
                    <span class="cancelOrder">取消</span>
                <% } %>
                <% if(status == 4){ %>
                    <form class="paymentForm" action="/micromall/pay/alipayapi.php" method="post" target="_blank">
                        
                        <input type="hidden" name="WIDout_trade_no" value="<%= cart_id %>"/>
                        <input type="hidden" name="WIDtotal_fee" value="<%= cart_total %>"/>
                        <input type="hidden" name="code" value="oyQi999IclGY9yfAAlzG4nUlDH3A"/>
                        <input type="hidden" name="orgid" value="1"/>
                        <input type="submit" class="paymentOrder" value="付款"/>
                    </form>
                <% } %>
            </div>
            <div class="orderResult-list" id="items-order-result">
                <div class="order-info">
                    <span>
                        订单号：<span id="order-no"><%= cart_id %></span>
                    </span>
                    <span class="date" style="float: right"></span>
                </div>
                <div class="order-list" id="item-order-list">
                    <ul></ul>
                </div>
                <div class="divider"></div>
                <div class="total-info">
                    <span>
                        运费：<span><%= parseFloat(freight||0).toFixed(2) %></span>元，共<span><%= parseFloat(cart_total).toFixed(2) %></span>元
                    </span>
                </div>				
            </div>
	</script>

	<!-- 警告弹窗视图模版 -->
	<script type="text/template" id="orderInfoPopupView-template">
            <div class="popup-header"></div>
            <div class="btn-group">
                <button class="btn">关闭</button>
            </div>
	</script>

	<!-- 确认弹窗视图模版 -->
	<script type="text/template" id="orderConfirmPopupView-template">
            <div class="popup-header"></div>
            <div class="popup-tips"></div>
            <div class="btn-group">
                <button class="btn" id="yes">确定</button>
                <button class="btn" id="no">取消</button>
            </div>
	</script>

	<script>
            var current_user = "111";
            // var user_status  = "NEW_USER";
            var user_status  = "CUSTOMER";
            var baseUrl = '/microfront/';
            // var cust = {"Customer":{"open_id":"oyQi999IclGY9yfAAlzG4nUlDH3A","org_id":"1","city":"","area":"","money":"0.00"}};
            var cust = {"Customer":{"open_id":"111","org_id":"1","city":"","area":"","money":"112.0"}};
            var organization = {"Organization":{"id":"1","name":"\u7231\u597D\u98DF","kf_phone":"075533100289","tip_content":"\u60a8\u7684\u8ba2\u5355\u6211\u4eec\u5c06\u5728\u9884\u5b9a\u7684\u914d\u9001\u65f6\u95f4\u6bb5\u9001\u8fbe\u3002","distribution_range":"tcl\u5927\u53a6\u9644\u8fd11000\u7c73\r\n\u817e\u8baf\u5927\u53a6\u9644\u8fd11000\u7c73","freight":"0.00"}};
            var organization = {"Organization": {"freight": "0.000000", "tip_content": "\u60a8\u7684\u8ba2\u5355\u6211\u4eec\u5c06\u5728\u4ee5\u4e0b\u65f6\u95f4\u6bb5\u9001\u8fbe<br />\n1\u3001\u7eff\u8272\u852c\u83dc\uff1a\u4e0b\u5355\u540e\u6b21\u65e5\u4e0b\u73ed\u524d\u9001\u8fbe<br />\n2\u3001\u597d\u98df\u6d77\u9c9c\uff1a\u4e0b\u5355\u540e\u6b21\u65e5\u4e0b\u73ed\u524d\u9001\u8fbe<br />\n3\u3001\u597d\u98df\u6709\u673a\uff1a\u4e0b\u5355\u540e\u7b2c\u4e09\u5929\u4e0b\u73ed\u524d\u9001\u8fbe<br />\n\u6ce8\uff1a\u7531\u4e8e\u6709\u673a\u852c\u83dc\u5168\u90e8\u7531\u4e91\u5357\u7a7a\u8fd0\u8fc7\u6765\uff0c\u4e3a\u4e86\u4fdd\u8bc1\u4ea7\u54c1\u65b0\u9c9c\uff0c\u9700\u8981\u63d0\u524d3\u5929\u9884\u8ba2\uff0c\u5e26\u6765\u4e0d\u4fbf\uff0c\u656c\u8bf7\u8c05\u89e3", "kf_phone": "15889613776", "distribution_range": "\u5357\u5c71\u79d1\u6280\u56ed\u5730\u94c1\u7ad9\u9644\u8fd11000\u7c73", "id": "1", "name": "\u7231\u597d\u98df"}};

            var deliveryTimes = [{"DeliveryTime": {"start_time": "16:00", "org_id": "1", "id": "5", "end_time": "18:00"}}];

            var catalogs = [{"Catalog": {"sort": "1", "status": "1", "name": "\u7eff\u8272\u852c\u83dc", "url": "url", "org_id": "1", "id": "11"}}, {"Catalog": {"sort": "2", "status": "1", "name": "\u597d\u98df\u6709\u673a", "url": "url", "org_id": "1", "id": "12"}}, {"Catalog": {"sort": "3", "status": "1", "name": "\u597d\u98df\u6d77\u9c9c", "url": "url", "org_id": "1", "id": "13"}}];
            var moreCatalogs = {};

            var items = {"11": [{"Goods": {"status": "1", "total": "4", "name": "\u767d\u83dc500g", "level": "2", "old_price": "8.000000", "price": "6.000000", "org_id": "1", "sales": "1", "cover_url": "/files/upfiles/20140625/1403693492370.jpg", "content": "", "catalog_id": "11", "servings": "1", "genre": "3", "zan_num": "40", "detail_url": "micromall/files/upfiles/20140625/1403693492371.jpg", "id": "37", "stime": "2014-03-18 15:45:30"}}, {"Goods": {"status": "1", "total": "0", "name": "\u767d\u841d\u535c 500g", "level": "1", "old_price": "11.000000", "price": "10.000000", "org_id": "1", "sales": "2", "cover_url": "/files/upfiles/20140604/1401895558793.jpg", "content": "", "catalog_id": "11", "servings": "1", "genre": "1", "zan_num": "27", "detail_url": "micromall/files/upfiles/20140604/1401895558794.jpg", "id": "36", "stime": "2014-03-18 15:45:30"}}], "13": [{"Goods": {"status": "1", "total": "7", "name": "\u8783\u87f9 300~450g", "level": "1", "old_price": "40.000000", "price": "35.000000", "org_id": "1", "sales": "3", "cover_url": "/files/upfiles/20140626/1403772532623.jpg", "content": "", "catalog_id": "13", "servings": "1", "genre": "3", "zan_num": "3", "detail_url": "micromall/files/upfiles/20140626/1403772532624.jpg", "id": "39", "stime": "2014-03-18 15:45:30"}}], "12": [{"Goods": {"status": "1", "total": "0", "name": "\u6709\u673a1", "level": "0", "old_price": "22.000000", "price": "22.000000", "org_id": "1", "sales": "1", "cover_url": "/files/upfiles/20140703/1404391370128.jpg", "content": "", "catalog_id": "12", "servings": "1", "genre": "3", "zan_num": "0", "detail_url": "micromall/files/upfiles/20140703/1404391370129.jpg", "id": "40", "stime": "2014-03-18 15:45:30"}}, {"Goods": {"status": "1", "total": "0", "name": "\u6709\u673a\u767d\u83dc 500g", "level": "1", "old_price": "30.000000", "price": "26.000000", "org_id": "1", "sales": "20", "cover_url": "/files/upfiles/20140625/1403693577991.jpg", "content": "", "catalog_id": "12", "servings": "1", "genre": "3", "zan_num": "32", "detail_url": "micromall/files/upfiles/20140625/1403693577992.jpg", "id": "34", "stime": "2014-03-18 15:45:30"}}, {"Goods": {"status": "1", "total": "53", "name": "\u6709\u673a\u767d\u841d\u535c 500g", "level": "2", "old_price": "28.000000", "price": "28.000000", "org_id": "1", "sales": "7", "cover_url": "/files/upfiles/20140625/1403693867187.jpg", "content": "", "catalog_id": "12", "servings": "1", "genre": "2", "zan_num": "30", "detail_url": "micromall/files/upfiles/20140625/1403693867188.jpg", "id": "35", "stime": "2014-03-18 15:45:30"}}, {"Goods": {"status": "1", "total": "0", "name": "\u6709\u673a\u9999\u8549\u897f\u846b\u82a6 500g", "level": "3", "old_price": "28.000000", "price": "28.000000", "org_id": "1", "sales": "2", "cover_url": "/files/upfiles/20140623/1403536233522.jpg", "content": "", "catalog_id": "12", "servings": "1", "genre": "1", "zan_num": "5", "detail_url": "micromall/files/upfiles/20140623/1403536233523.jpg", "id": "38", "stime": "2014-03-18 15:45:30"}}]};
            var slctidx = 1;

            var cities = [{"Address":{"id":"381","name":"\u6df1\u5733\u5e02","parent_id":"380","level":"2","org_id":"1","hat_id":"440300"}}];
            // var areas = {"381":[{"Address":{"id":"382","name":"\u5B9D\u5B89\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}},{"Address":{"id":"383","name":"\u5357\u5C71\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}},{"Address":{"id":"601","name":"\u798F\u7530\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}},{"Address":{"id":"700","name":"\u7F57\u6E56\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}}]};
            var areas = {"381":[{"Address":{"id":"383","name":"\u5357\u5C71\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}}, {"Address":{"id":"382","name":"\u5B9D\u5B89\u533A","parent_id":"381","level":"3","org_id":"1","hat_id":null}}]};
            var tradeTime = [];
            // widget.init(data_from_django);
	</script>
        
	<script src="js/components/jquery/jquery.min.js"></script>
	<script src="js/components/underscore/underscore.min.js"></script>
	<script src="js/components/backbone/backbone.min.js"></script>	
	<script src="js/components/backbone/backbone.touch.js"></script>
	<script src="js/models/models.js?5"></script>
	<script src="js/views/views.js?5"></script>
	<script src="js/application.js?5"></script>

	<link rel="stylesheet" href="css/iphone.css">	<script>
        $(document).on('click', '.dail-small', function(){
            window.location.href = "tel:" + organization.Organization.kf_phone;
            if(navigator.userAgent.toLowerCase().indexOf("iphone") === -1){
                $(".dail-small").text(organization.Organization.kf_phone);
            }
        });

        $(document).on('click', '.zan', function(){
		var $i=$(this).children(".zan_num");
		var $j=$(this).children(".zan_span");
                var n=parseInt($i.text());
                var id = $(this).parents('.item').attr('id');

                if (1 != parseInt($i.val())) {
		    $.post("zan/",{zan:id}, function(data){$i.text(n+1);$j.css("background-image", "url(img/zaned.png)");$i.val("1");});
                }
        });
        
        if(sc.getWechatId() && sc.getWechatId() != getUuid()){
            setCookie('wechat_id','',-1);
        }

        $('.types ul li').removeClass('active');
        $("#m13").addClass("active");
</script>


</body></html>
