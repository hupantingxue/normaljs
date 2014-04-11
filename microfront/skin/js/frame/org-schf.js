function bading(url){
    $.get(url, function(result){alert("菜单已重新生成!");});
}
function saveProvince(){
        var hatid =  $("#province").val();
	var name=$("#province").find("option:selected").text();
	if(hatid=="0"){
		alert("请选择省");
		return;
	}
        var cityHatId =  $("#city").val();
	var city=$("#city").find("option:selected").text();
	if(cityHatId=="0"){
		alert("请选择市");
		return;
	}
	var str=$("#area").val();
	if(str==""){
		alert("请填写详细地址");
		return;
	}
	$.ajax({ 
        type: "post", 
        url: "../org/address-ajax.php", 
		data : {
			id:0,parentid:0,name:name,act:'province',hatid:hatid
		},
        dataType: "json", 
        success: function (data) { 
		   if(data.status==1){
		   		saveCity(data.id);
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function saveCity(parentid){
        var hatid =  $("#city").val();
	var name=$("#city").find("option:selected").text();
	$.ajax({ 
        type: "post", 
        url: "../org/address-ajax.php", 
		data : {
			id:0,parentid:parentid,name:name,act:'city',hatid:hatid
		},
        dataType: "json", 
        success: function (data) {
		   if(data.status==1){
				var str=$("#area").val();
				var pid = data.id;
				saveArea(pid,str);
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function saveArea(parentid,names){
	$.ajax({ 
        type: "post", 
        url: "../org/address-ajax.php", 
		data : {
			id:0,parentid:parentid,names:names,act:'area'
		},
        dataType: "json", 
        success: function (data) {
			alert(data.result); 
		    if(data.status==1){
				location.href ="../org/address-list.php";
		    }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delAddress(id){
	$.ajax({ 
        type: "post", 
        url: "../org/address-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/address-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function editTime(id,stime,etime){
	$("#id").val(id);
	$("#stime").val(stime);	
	$("#etime").val(etime);	
}

function saveTime(){
	var id = $("#id").val();
	if(checkNull("stime")){
		alert("请输入开始时间");
		$("#stime").focus();
		return;
	}
	if(checkNull("etime")){
		alert("请输入结束时间");
		$("#etime").focus();
		return;
	}
	var stime = $("#stime").val();
	var etime = $("#etime").val();
	$.ajax({ 
        type: "post", 
        url: "../org/time-ajax.php", 
		data : {
			id : id,
			stime : stime,
			etime : etime,
			act : "edit"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		    if(data.status==1){
		   		location.href ="../org/time-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delTime(id){
	$.ajax({ 
        type: "post", 
        url: "../org/time-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/time-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function editCatalog(id,name,url){
	$("#id").val(id);
	$("#name").val(name);
	$("#url").val(url);	
}

function saveCatalog(){
	if(checkNull("name")){
		alert("请输入目录名称");
		$("#name").focus();
		return;
	}
	if(checkNull("url")){
		alert("请输入目录地址");
		$("#url").focus();
		return;
	}
	var id = $("#id").val();
	var name = $("#name").val();
	var url = $("#url").val();
	$.ajax({ 
        type: "post", 
        url: "../org/catalog-ajax.php", 
		data : {
			id : id,
			name : name,
			url : url,
			act : "edit"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		    if(data.status==1){
		   		location.href ="../org/catalog-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delCatalog(id){
	$.ajax({ 
        type: "post", 
        url: "../org/catalog-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/catalog-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function saveCatalogSort(val,id){
	if(!isPositiveIntegers(val)){
		$("#sort_"+id).val(1);
		return ;
	}
	$.ajax({ 
        type: "post", 
        url: "../org/catalog-ajax.php", 
		data : {
			id : id,
			val : val,
			act : "sort"
		}
    });
}
function saveCatalogStatus(obj,id){
	var val=2;
	if(obj.checked == true){
		val=1;
	}
	$.ajax({ 
        type: "post", 
        url: "../org/catalog-ajax.php", 
		data : {
			id : id,
			val : val,
			act : "status"
		} 
    });
}
function editKeyword(id,keyowrd,descn){
	$("#id").val(id);
	$("#keyword_name").val(keyowrd);
        descn = descn.replaceAll("<br/>","\n");
	$("#descn").val(descn);	
}

function saveKeyword(){
	if(checkNull("keyword_name")){
        alert("请输入关键字");
		$("#keyword_name").focus();
		return;
    }
	var type = $("#type").val();
	var material_id = $("#material_id").val();
	if(type == "1"){
		if(checkNull("descn")){
			alert("请输入回复内容");
			$("#descn").focus();
			return;
		}
	}else{
		if(checkNull("material_title")){
			alert("请输入回复内容");
			$("#material_title").focus();
			return;
		}
	}
	var id = $("#id").val();
	var keyword = $("#keyword_name").val();
	var descn = $("#descn").val();
	$.ajax({ 
        type: "post", 
        url: "../org/keyword-ajax.php", 
		data : {
			id : id,
			keyword : keyword,
			descn : descn,
			type : type,
			material_id : material_id,
			act : "edit"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		    if(data.status==1){
		   		location.href ="../org/keyword-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delKeyword(id){
	$.ajax({ 
        type: "post", 
        url: "../org/keyword-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/keyword-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function editAttention(id,descn){
	$("#id").val(id);
        descn = descn.replaceAll("<br/>","\n");
	$("#descn").val(descn);	
}

function saveAttention(){
	var type = $("#type").val();
	var material_id = $("#material_id").val();
	if(type == "1"){
		if(checkNull("descn")){
			alert("请输入回复内容");
			$("#descn").focus();
			return;
		}
	}else{
		if(checkNull("material_title")){
			alert("请输入回复内容");
			$("#material_title").focus();
			return;
		}
	}
	var id = $("#id").val();
	var descn = $("#descn").val();
	$.ajax({ 
        type: "post", 
        url: "../org/attention-ajax.php", 
		data : {
			id : id,
			descn : descn,
			type : type,
			material_id : material_id,
			act : "edit"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		    if(data.status==1){
		   		location.href ="../org/attention-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delAttention(id){
	$.ajax({ 
        type: "post", 
        url: "../org/attention-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/attention-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function editMenuName(id,name){
	$("#id").val(id);
	$("#mname").val(name);	
}


function saveMenuName(){
	var id = $("#id").val();
	var name = $("#mname").val();
        if(checkNull("mname")){
            alert("菜单名称不能为空");
            return;
        }
	$.ajax({ 
        type: "post", 
        url: "../org/menu-ajax.php", 
		data : {
			id : id,
			name : name,
			act : "updatename"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
				location.href ="../org/menu-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function editMenu(id,name,descn,operate){
	if(name=='-1'){
		id = $("#id").val();
		if(operate=='admin'){
			location.href ="../admin/menu-edit.php?id="+id;
		}else{
			location.href ="../org/menu-edit.php?id="+id;
		}
	}
	$("#id").val(id);
	$("#name").val(name);
        descn = descn.replaceAll("<br/>","\n");
	$("#descn").val(descn);	
}

function saveMenu(operate){
	var type = $("#type").val();
	var material_id = $("#material_id").val();
	if(type == "1"){
		if(checkNull("descn")){
			alert("请输入回复内容");
			$("#descn").focus();
			return;
		}
	}else{
		if(checkNull("material_title")){
			alert("请输入回复内容");
			$("#material_title").focus();
			return;
		}
	}
	var id = $("#id").val();
	var descn = $("#descn").val();
	var url = "";
	if(operate=='admin'){
		url="../admin/menu-ajax.php";
	}else{
		url="../org/menu-ajax.php";
	}
	$.ajax({ 
        type: "post", 
        url: url, 
		data : {
			id : id,
			descn : descn,
			type : type,
			material_id : material_id,
			act : "edit"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		    if(data.status==1){
				if(operate=='admin'){
					location.href ="../admin/menu-list.php";
				}else{
					location.href ="../org/menu-list.php";
				}
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

//选取素材
function selectMaterial(){
	var args = showDialog(new Object(),"materials.php",1000,600);
        if(args == undefined) { 
            args = window.returnValue; 
        }
	if(args!=null){
		$("#material_id").val(args.id);
		$("#material_title").val(args.title);
	}
}
//选中
function selected(id,title){
    var args = new Object();
    args.id = id;
    args.title = title;
    //for chrome 
    var isChrome = window.chrome;
    if(window.opener != undefined && isChrome) { //window.opener的值在谷歌浏览器下面不为空，在IE/火狐下面是未定义，由此判断是否是谷歌浏览器 
        window.opener.returnValue = args; //谷歌浏览器下给返回值赋值的方法
        window.opener.close(); //这里必须关闭一次，否则执行下面的window.close()无法关闭弹出窗口，因为谷歌浏览器下弹出窗口是个新的window     
    }else { 
        window.returnValue = args; //这种赋值方法兼容IE/火狐，但不支持谷歌浏览器 
    }
    window.close();
}

function provinceChange(val){
	if (val == 0) {
		$("#city").empty();
		$("#city").append("<option value='0'>--请先选择省/直辖市--</option>");
		$("#areaDiv").empty();
		return;
	}
	$.ajax({
		type : "post",
		async : false,
		url : "../org/address-select.php",
		data : {
			val : val,
			act : 'city'
		},
		dataType : 'json',
		success : function(data) {
			$("#city").empty();
			$("#city").append("<option value='0'>--请先选择省/直辖市--</option>");
			for ( var i = 0; i < data.length; i++) {
				var val = data[i].id;
				var text = data[i].name;
				$("#city").append("<option value='" + val + "'>" + text + "</option>");
			}
		},
		error : function() {
			alert("操作时,出现异常,请联系管理员!");
		}
	});
}

function editHandsel(id,money,handsel){
	$("#id").val(id);
        if(money==0){
           $("#money").val(''); 
        }else{
            $("#money").val(money);
        }
        if(handsel==0){
           $("#handsel").val(''); 
        }else{
            $("#handsel").val(handsel);		
        }
}

function saveHandsel(){
	var id = $("#id").val();
	var money = $("#money").val();
	var handsel = $("#handsel").val();
	if(!isDouble(money)){
		alert("充值金额只能保留小数点后两位或您输入的不是数值");
		$("#money").focus();
		return;
	}
	if(!isDouble(handsel)){
		alert("赠送比只能保留小数点后两位或您输入的不是数值");
		$("#handsel").focus();
		return;
	}
	$.ajax({ 
        type: "post", 
        url: "../org/handsel-ajax.php", 
		data : {
			id : id,
			money : money,
			handsel : handsel,
			act : "save"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
				location.href ="../org/handsel-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}
function delHandsel(id){
	$.ajax({ 
        type: "post", 
        url: "../org/handsel-ajax.php", 
		data : {
			id : id,
			act : "del"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
		   if(data.status==1){
		   		location.href ="../org/handsel-list.php";
		   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}
function saveTradeTime(){
    var id = $("#id").val();
    var status = getRadioValue("status");
    if(status==undefined){
        alert("请选择状态");
        return;
    }
    var week_num = $("#week_num").val();
    if(status==1){
        if(checkNull("start_time")){
            alert("把开始时间息写上吧！");
            return;
        }
        if(checkNull("end_time")){
            alert("把结束时间息写上吧！");
            return;
        }
        if(checkNull("end_time")){
            alert("把营业时间外的提示信息写上吧！");
            return;
        }
    }
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    start_time = start_time.replace(":","");
    start_time = start_time.replace(":","");
    end_time = end_time.replace(":","");
    end_time = end_time.replace(":","");
    var tips = $("#tips").val();
    $.ajax({ 
        type: "post", 
        url: "../org/trade-time-ajax.php", 
		data : {
			id : id,
			week_num : week_num,
			start_time : start_time,
			end_time : end_time,
                        status : status,
			tips : tips,
			act : "save"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
        },error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}


function savePaymentMode(){
    var id = $("#id").val();
    var status = getRadioValue("status");
    var pay_mode = $("#pay_mode").val();
    var tips = $("#tips").val();
    if(status==2){
       if(checkNull("tips")){
            alert("把消息提示写上吧，要不别人不知道为什么不能支付哦！");
            return;
        }
    }
    $.ajax({ 
        type: "post", 
        url: "../org/payment-mode-ajax.php", 
		data : {
			id : id,
			pay_mode : pay_mode,
                        status : status,
			tips : tips,
			act : "save"
		},
        dataType: "json", 
        success: function (data) { 
           alert(data.result);
        },error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function getRadioValue(radioName){ 
    var obj=document.getElementsByName(radioName);
    if(obj!=null){
        for(var i=0;i<obj.length;i++){
            if(obj[i].checked){
                return obj[i].value;            
            }
        }
    }
    return -1;
}