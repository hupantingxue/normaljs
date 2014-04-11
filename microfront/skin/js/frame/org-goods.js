function operate(id,act,val){
	if(val=='上架'){
		val = 1;
	}
	if(val=='下架'){
		val = 2;
	}
	$.ajax({ 
        type: "post", 
        url: "../org/goods-ajax.php", 
		data : {
			id : id,
			int_val : val,
			act : act
		},
        dataType: "json", 
        success: function (data) { 
			if(data.status == 1 && act == "status"){
				if(val==2){
					$("#sxjia_"+id).attr("class","btn-info");
					$("#sxjia_"+id).val("上架");
				}else{
					$("#sxjia_"+id).attr("class","btn-danger");
					$("#sxjia_"+id).val("下架");
				}
			}
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

//开始上传
function startUpload(val) { 
	$("#processing_"+val).text("在正上传....");
	return true; 
} 

//结束上传
function stopUpload(rel,fileName,val){ 
	var msg; 
	switch (rel) { 
		case 0: 
			var imgUrl = base_url + fileName;
			if(val==1){
				$("#fmt").attr("src",imgUrl);
				$("#cover_url").val(fileName);
			}
			if(val==2){
				$("#xqt").attr("src",imgUrl);
				$("#preview_xqt").attr("src",imgUrl);
				$("#detail_url").val(fileName);
			}
			msg = "上传成功"; 
			break; 
		case 1: 
			msg = "上传的文件超过限制,重新选择文件..."; 
			break; 
		case 2: 
			msg = "只能上传图片,重新选择文件..."; 
			break; 
		default: 
			msg = "上传文件失败"; 
	} 
	$("#processing_"+val).text(msg);
} 


//提交上传
function submitFileUploadForm(val){
	$("#uploadFileForm_"+val).submit();
}

function saveGoods(operate){
    if(checkNull("cover_url")){
        alert("请上传封面图片");
		$("#cover_url").focus();
		return;
    } 
	if(checkNull("detail_url")){
        alert("请上传详情图片");
		$("#detail_url").focus();
		return;
    } 
    if(checkNull("name")){
        alert("请输入商品名称");
		$("#name").focus();
		return;
    }
    if(checkNull("price") && checkNull("old_price")){
        alert("请输入优惠价格或商品原价");
	$("#price").focus();
	return;
    }
	var cover_url = $("#cover_url").val();
	var detail_url = $("#detail_url").val();
	var name = $("#name").val();
        
	var price = $("#price").val();
	if(!checkNull("price") && !isDouble(price)){
		alert("优惠价格只能保留小数点后两位或您输入的不是数值");
		$("#price").focus();
		return;
	}
	var old_price = $("#old_price").val();
	if(!checkNull("old_price") && !isDouble(old_price)){
		alert("商品原价只能保留小数点后两位或您输入的不是数值");
		$("#old_price").focus();
		return;
	}
        if(old_price=='' && price!=''){
            old_price = price;
        }
        if(old_price!='' && price==''){
            price = old_price;
        }
        if(parseInt(old_price)<parseInt(price)){
            alert("优惠价还比商品原价要高，不太好吧!");
            $("#old_price").focus();
            return;
        }
	var content = pro.getContent();
	if(content==''){
		alert("请填写详情内容");
		return;
	}
	var catalog_id = $("#catalog_id").val();
	var id = $("#id").val();
	$.ajax({ 
        type: "post", 
        url: "../org/goods-ajax.php", 
		data : {
			id : id,
			cover_url : cover_url,
			detail_url : detail_url,
			name : name,
			price : price,
			old_price : old_price,
			content : content,
			catalog_id : catalog_id,
			act : 'save'
		},
        dataType: "json", 
        success: function (data) { 
		   if(data.status==1){
                    alert(data.result);
                    if(operate==2){
                        location.href ="../org/goods-food-ingredients.php?goodid="+data.id;
                    }else{
                       location.href ="../org/goods-list.php";
                    }
                   }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

var rowCount=1;
function addFootRow(){ 
    rowCount = $("#foodTable").find("tr").length;
    var rowTemplate = '<tr class="tr_'+rowCount+'"><td><input type="text" id="name_'+rowCount+'" name="names"></td><td class="cl1"><input type="text" id="quantity_'+rowCount+'" name="quantitys">';
    rowTemplate +='<input type="hidden" name="units" id="unit_'+rowCount+'" value="1">';
    rowTemplate +='<input type="radio" style="margin-bottom:15px;" name="danweis_'+rowCount+'" value="1" onClick="$(\'#unit_'+rowCount+'\').val(1);" checked>克';
    rowTemplate +='<input type="radio" style="margin-bottom:15px;" name="danweis_'+rowCount+'" value="2" onClick="$(\'#unit_'+rowCount+'\').val(2);">包';
    rowTemplate +='<input type="radio" style="margin-bottom:15px;" name="danweis_'+rowCount+'" value="3" onClick="$(\'#unit_'+rowCount+'\').val(3);">个';
    rowTemplate +='<input type="radio" style="margin-bottom:15px;" name="danweis_'+rowCount+'" value="4" onClick="$(\'#unit_'+rowCount+'\').val(4);">粒';
    rowTemplate +='</td><td class="cl1"><a href="javascript:delRow('+rowCount+')"><i class="icon-remove"></i></a></td></tr>';
    var row = $("#tab tr:last");
    var $tr=$("#foodTable tr").eq(-1);
    $tr.after(rowTemplate);
    rowCount++;
}

function delFood(id,row){
    $.ajax({ 
        type: "post", 
        url: "../org/goods-ajax.php", 
		data : {
			id : id,
			act : 'footdel'
		},
        dataType: "json", 
        success: function (data) { 
		if(data.status==1){
                    $("tr[id=tr_"+row+"]").remove();
                    alert(data.result);
                }
        },
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

function delRow(row){
   $("#foodTable .tr_"+row).remove();
   rowCount--;
}
function saveFood(operate,goodsid){
    var names = "",quantitys="",units="";
    var isNull=true;
    $("input[name='names']").each( 
        function(){ 
            var val = $(this).val();
            val = val.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
            if(val==''){
                isNull=false;
            }
            names+=val+"|"; 
        }  
    );
    var isInt=true;
    $("input[name='quantitys']").each( 
        function(){ 
            var val = $(this).val();
            val = val.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
            if(isPositiveIntegers(val)){
               quantitys+=val+"|"; 
            }else{
                isInt=false;
            }
        }  
    );
    $("input[name='units']").each( 
        function(){ 
            units+=$(this).val()+"|"; 
        }  
    );
    if(!isNull){
        alert("名称不能为空");
        isNull = true;
        return;
    }
    if(!isInt){
        alert("份量只能是正整数");
        isInt = true;
        return;
    }
    if(names=='' || quantitys==''){
        alert("名称或份量不能为空");
        return;
    }else{
        names = names.substring(0,names.length-1);
        quantitys = quantitys.substring(0,quantitys.length-1);
    }
    $.ajax({ 
        type: "post", 
        url: "../org/goods-ajax.php", 
	data : {
			goodsid : goodsid,
			type : operate,
                        names : names,
                        quantitys : quantitys,
                        units : units,
			act : 'footadd'
	},
        dataType: "json", 
        success: function (data) { 
            if(data.status==1){
                alert(data.result);
                if(operate==1){
                    location.href ="../org/goods-food-ingredients.php?goodid="+goodsid;
                }else{
                    location.href ="../org/goods-food-accessories.php?goodid="+goodsid;
                }
            }
        },error: function (XMLHttpRequest, textStatus, errorThrown) { 
            alert(errorThrown); 
        } 
    });
}

