var base_url = "http://www.qq-green.com/micromall/";
/**
 * 弹出dialog窗口
 * 
 * @param url
 * @param width
 * @param height
 * @returns
 */
function showDialog(params, url, width, height) {
	var returnArgs = window.showModalDialog(url, params, "dialogWidth=" + width
			+ "px;dialogHeight=" + height
			+ "px;help:no;scroll:yes;resizable:no;status:0;");
	return returnArgs;
}

// 全选
function selectAll(name) {
	$("input[name='" + name + "']").each(function() {
		if ($(this).attr("checked")) {
			$(this).attr("checked", false);
		} else {
			$(this).attr("checked", true);
		}
	});
}

// 判判是否为空,传入input的id
function checkNull(inId) {
	var flag = false;
	if ($("#" + inId) == null) {
		flag = true;
	}
	var val = $("#" + inId).val();
	val = val.replace(/^\s+|\s+$/g, '');
	if (val == "") {
		flag = true;
	}
	return flag;
}
//判断值是否为正整数
function isPositiveIntegers(val){
     var re = /^[1-9]+[0-9]*]*$/
     if (!re.test(val)){
        return false;
     }
	 return true;
}

//判断值是否为正浮点数 
function isDouble(val){
	 var re = /^\d+[\.\d]?\d{0,2}$/;
	 if (!re.test(val)){
        return false;
     }
	 return true;
}

String.prototype.replaceAll = stringReplaceAll;
function stringReplaceAll(AFindText,ARepText){
    raRegExp = new RegExp(AFindText,"g");
    return this.replace(raRegExp,ARepText)
}