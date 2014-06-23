var app = app || {};
app.ItemView = Backbone.View.extend({
	className: 'item',
	template: _.template($('#item-template').html()),
	events: {
		'click .item-image': 'select',
		'click .select-shadow': 'unselect',
		'click .item-detail': 'showDetail',
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.attr('id', 'item-' + this.model.get('Goods').id);
		return this
	},
	select: function() {
		this.$el.find('.select-shadow').css('display', 'block');
		if ($('.shopping-cart').css('display') == 'none') {
			$('.shopping-cart').css('display', 'block')
		}
		app.shoppingCart.get('items').add(this.model);
		app.shoppingCart.get('items').date = this.model.get('date')
	},
	unselect: function() {
		this.$el.find('.select-shadow').css('display', 'none');
		app.shoppingCart.get('items').remove(this.model);
		if (app.shoppingCart.get('items').length == 0) {
			$('.shopping-cart').css('display', 'none')
		}
	},
	imgLazyLoad: function() {
		var that = this;
		var $img = this.$el.find('.item-image > img');
		var url = $img.attr('lazy-src');
		var priority = this.model.get('Goods').genre;
		var sales = this.model.get('Goods').sales;
		var total = this.model.get('Goods').total;
                // if (parseInt(sales) >= parseInt(total)) {
                if (0 >= parseInt(total)) {
		    this.$el.find('.soldout-shadow').css('display', 'block');
                }

		if (url != undefined) {
			var img = new Image();
			img.onload = function() {
				$img.attr('src', url);
				$img.css({
					'width': '100%',
					'height': '110px',
					'margin-top': '0'
				});

                                if (priority == '3') {
			            $img.css('height', '180px');
				    that.$el.find('.item-title').append('<span style="background: #5bc0de;color: white;padding: 2px 5px;margin-left: 10px;border-radius: 5px;">今日推荐</span>')
				}

				/* if (priority == '2' || priority == '3') {
					$img.css('height', '180px');
					if (priority == "3") {
						that.$el.find('.item-title').append('<span style="background: #5bc0de;color: white;padding: 2px 5px;margin-left: 10px;border-radius: 5px;">今日特价</span>')
					} else {
						that.$el.find('.item-title').append('<span style="background: #5bc0de;color: white;padding: 2px 5px;margin-left: 10px;border-radius: 5px;">今日推荐</span>')
					}
				} */

			}
			img.src = url
		}
	},
	showDetail: function() {
		var that = this;
		$.ajax({
			url: baseUrl + 'items/' + this.model.get('Goods').id + '.json',
			success: function(data) {
				var item = new app.Item(data.rt_obj.data);
				$(".container").css('display', 'none');
				var itemDetailView = new app.ItemDetailView({
					model: item,
					parent: that
				})
			},
			error: function(data) {
				console.log(data)
			}
		})
	}
});
app.ItemViewWithoutImg = Backbone.View.extend({
	className: 'item',
	template: _.template($('#item-template-no-img').html()),
	events: {
		'click .item-image': 'select',
		'click .select-shadow-no-img': 'unselect',
		'click .item-detail': 'showDetail'
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.attr('id', 'item-' + this.model.get('Goods').id);
		this.imgLazyLoad();
		return this
	},
	select: function() {
		this.$el.find('.select-shadow-no-img').css('display', 'block');
		if ($('.shopping-cart').css('display') == 'none') {
			$('.shopping-cart').css('display', 'block')
		}
		app.shoppingCart.get('items').add(this.model)
	},
	unselect: function() {
		this.$el.find('.select-shadow-no-img').css('display', 'none');
		app.shoppingCart.get('items').remove(this.model);
		if (app.shoppingCart.get('items').length == 0) {
			$('.shopping-cart').css('display', 'none')
		}
	},
	imgLazyLoad: function() {
		var $img = this.$el.find('.item-image > img');
		var url = $img.attr('lazy-src');
		var priority = this.model.get('Cookbook').priority;
		var sales = this.model.get('Goods').sales;
		var total = this.model.get('Goods').total;
                // if (parseInt(sales) >= parseInt(total)) {
                if (0 >= parseInt(total)) {
		    this.$el.find('.soldout-shadow-no-img').css('display', 'block');
                }

		if (url != undefined) {
			var img = new Image();
			img.onload = function() {
				$img.attr('src', url);
				$img.css({
					'width': '100%',
					'height': '110px',
					'margin-top': '0'
				});
				if (priority == '1' || priority == '2') {
					$img.css('height', '180px');
					if (priority == "1") {
						that.$el.find('.item-title').append('<span style="background: #5bc0de;color: white;padding: 2px 5px;margin-left: 10px;border-radius: 5px;">今日特价</span>')
					} else {
						that.$el.find('.item-title').append('<span style="background: #5bc0de;color: white;padding: 2px 5px;margin-left: 10px;border-radius: 5px;">今日推荐</span>')
					}
				}
			}
			img.src = url
		}
	},
	showDetail: function() {
		var that = this;
		$.ajax({
			url: baseUrl + 'items/' + this.model.get('Goods').id + '.json',
			success: function(data) {
				var item = new app.Item(data.rt_obj.data);
				$(".container").css('display', 'none');
				var itemDetailView = new app.ItemDetailView({
					model: item,
					parent: that
				})
			},
			error: function(data) {
				console.log(data)
			}
		})
	}
});
app.LoginView = Backbone.View.extend({
	className: 'container',
	id: 'login-container',
	template: _.template($("#loginView-template").html()),
	events: {
		'click #login': 'login',
//		'click #forget': 'getPassword',
		'click #signin': 'signIn',
		'click .back': 'back'
	},
	initialize: function(options) {
		if (options && options.backTo) {
			this.backTo = options.backTo
		}
		$('.main-container').append(this.render().el)
	},
	render: function() {
		this.$el.html(this.template());
		return this
	},
	login: function() {
		var that = this;
		$(".login-tips").hide();
		$.ajax({
			url: baseUrl + 'home/login/' + that.getUuid(),
			type: 'post',
			data: {
				'username': $('input[name=account]').val(),
				'password': $('input[name=password]').val()
			},
			success: function(data) {
				var rt_obj = eval('(' + data + ')');
				if (rt_obj.code == 0) {
					setCookie("wechat_id", current_user, 100);
					that.$el.remove();
					$("#" + that.backTo).show()
				} else if (rt_obj.code == 2) {
					if (that.$el.find('.warning').length > 0) {} else {
						that.$el.find('.login-header').after("<p class=\"warning\">^_^用户名或密码错误，请重新输入</p>")
					}
				}
			},
			error: function(data) {
				console.log('login failed')
			}
		})
	},
//	getPassword: function() {
//		this.$el.hide();
//		var forgetView = new app.ForgetView();
//		$(".main-container").append(forgetView.render().el)
//	},
	signIn: function() {},
	back: function() {
		var that = this;
		that.$el.remove();
		$('#' + that.backTo).show()
	},
	getUuid: function() {
		return (function() {
			var search = window.location.search;
			var arrStr = search.substr(1, search.length).split('&');
			for (var i = 0; i < arrStr.length; i++) {
				var temp = arrStr[i].split('=');
				if (temp[0] == 'code') {
					return unescape(temp[1])
				}
			}
		})()
	},
});
app.RegisterView = Backbone.View.extend({
	className: 'container',
	id: 'register-container',
	template: _.template($("#registerView-template").html()),
	events: {
		'click #register': 'register',
		'click .back': 'back'
	},
	initialize: function(options) {
		if (options && options.backTo) {
			this.backTo = options.backTo
		}
		$('.main-container').append(this.render().el)
	},
	render: function() {
		this.$el.html(this.template());
		return this
	},
	register: function() {
		var that = this;
		if (that.inputValidate()) {
			console.log('validate success');
			$.ajax({
				url: baseUrl + 'home/register/' + that.getUuid(),
				// type: 'get',
				type: 'post',
				data: {
                                    'name': that.$el.find('input[name=name]').val()
                                    ,'username': that.$el.find('input[name=account]').val()
                                    , 'sex': $("#select_sex option:selected").text()
//                                    , 'password': that.$el.find('input[name=password]').val()
//                                    ,'email': that.$el.find('input[name=email]').val()
				},
				success: function(data) {
					var data = eval('(' + data + ')');
					if (data.code == 0) {
						var popupView = new app.OrderInfoPopupView({
							msg: '注册成功, 3秒后自动登录'
						});
						that.$el.append(popupView.render().el);
						setTimeout(function() {
							that.$el.remove();
							user_status = "CUSTOMER";
							setCookie("wechat_id", current_user, 100);
							$("#" + that.backTo).show()
						}, 3000)
					} else if (data.code == 1) {
						var popupView = new app.OrderInfoPopupView({
							msg: data.msg
						});
						that.$el.append(popupView.render().el)
					} else if (data.code == 2) {
						var popupView = new app.OrderInfoPopupView({
							msg: data.msg
						});
						that.$el.append(popupView.render().el)
					}
				},
				error: function() {
					console.log('ajax error')
				}
			})
		}
	},
	back: function() {
		var that = this;
		that.$el.remove();
		$('#' + that.backTo).show()
	},
	inputValidate: function() {
		var that = this;
		var un = that.$el.find('input[name=account]').val(),
//			pw = that.$el.find('input[name=password]').val(),
//			repw = that.$el.find('input[name=repassword]').val(),
//			email = that.$el.find('input[name=email]').val(),
                        name = that.$el.find('input[name=name]').val();
		var pwPattern = /^(\w){6,20}$/,
			emailPattern = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
		if (name == "") {
			var popup = new app.OrderInfoPopupView({
				msg: '姓名不能为空'
			});
			that.$el.append(popup.render().el);
			return false;
		} else if (un == "") {
			var popup = new app.OrderInfoPopupView({
				msg: '手机不能为空'
			});
			that.$el.append(popup.render().el);
			return false;
		} 
//                else if (!pwPattern.exec(pw)) {
//			var popup = new app.OrderInfoPopupView({
//				msg: '密码长度不符合要求（6-20位）'
//			});
//			that.$el.append(popup.render().el);
//			return false;
//		} else if (pw != repw) {
//			var popup = new app.OrderInfoPopupView({
//				msg: '两次输入的密码不一致'
//			});
//			that.$el.append(popup.render().el);
//			return false;
//		} else if (!emailPattern.exec(email)) {
//			var popup = new app.OrderInfoPopupView({
//				msg: '邮箱地址不正确'
//			});
//			that.$el.append(popup.render().el);
//			return false;
//		} else if (pwPattern.exec(pw) && emailPattern.exec(email) && (pw == repw)) {
//			return true;
//		}
		return true;
	},
	getUuid: function() {
		return (function() {
			var search = window.location.search;
			var arrStr = search.substr(1, search.length).split('&');
			for (var i = 0; i < arrStr.length; i++) {
				var temp = arrStr[i].split('=');
				if (temp[0] == 'code') {
					return unescape(temp[1])
				}
			}
		})()
	}
});
app.ForgetView = Backbone.View.extend({
	className: 'container',
	id: 'forget-container',
	template: _.template($("#forgetPasswordView-template").html()),
	events: {
		'click #getPassword': 'submit',
		'click .back': 'back'
	},
	initialize: function() {
		$('.main-container').append(this.render().el)
	},
	render: function() {
		this.$el.html(this.template());
		return this
	},
	submit: function() {
		var that = this;
		$.ajax({
			url: baseUrl + 'home/forget/' + that.getUuid(),
			method: 'post',
			data: {
				'username': $('#forget-container input[name=account]').val(),
				'email': $('#forget-container input[name=email]').val()
			},
			success: function(data) {
				var dataObj = eval("(" + data + ")");
				var popupView = new app.OrderInfoPopupView({
					msg: dataObj.message
				});
				that.$el.append(popupView.render().el)
			},
			error: function(data) {
				console.log(data);
				console.log('login failed')
			}
		})
	},
	back: function() {
		this.$el.remove();
		$('#login-container').show()
	},
	getUuid: function() {
		return (function() {
			var search = window.location.search;
			var arrStr = search.substr(1, search.length).split('&');
			for (var i = 0; i < arrStr.length; i++) {
				var temp = arrStr[i].split('=');
				if (temp[0] == 'code') {
					return unescape(temp[1])
				}
			}
		})()
	},
});
app.ItemDetailView = Backbone.View.extend({
	className: 'container',
	id: 'itemsdetail-container',
	template: _.template($('#itemDetailView-template').html()),
	events: {
		'click .back': 'back',
		'click .addItem': 'add',
		'click .backToTop': 'backToTop'
	},
	initialize: function(options) {
		this.parent = options.parent;
		$(window).scrollTop(0);
		$('.main-container').append(this.render().el);
		sc.dropdown('itemsdetail-container', '.user');
		this.$el.append(new app.ShoppingCartView({
			model: app.shoppingCart
		}).render().el);
		this.resizePic();
		if (app.shoppingCart.get('count') > 0) {
			if (this.$el.find('.shopping-cart').css('display') == 'none') {
				this.$el.find('.shopping-cart').css('display', 'block')
			}
		}
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		this.$el.find('.detail-content').find('table').addClass('steps').attr('border', 0);
		return this
	},
	resizePic: function() {
		var imgs = this.$el.find('.detail-content').find('img'),
			width = $('.detail-content').find('table').width() * 0.35;
		imgs.each(function() {
			//$(this).css('height', width + 'px')
		})
	},
	add: function() {
		if (app.shoppingCart.get('items').get(this.model.get('Goods').id)) {
			var popup = new app.OrderInfoPopupView({
				msg: "已加入购物车，请前往购物车查看"
			});
			this.$el.append(popup.render().el)
		} else {
			this.parent.select()
		}
	},
	backToTop: function() {
		$(window).scrollTop(2)
	},
	back: function() {
		this.$el.remove();
		$('#menu-container').css('display', 'block')
	}
});

app.ItemListView = Backbone.View.extend({
	className: 'items',
	hasPic: false,
	viewCollection: null,
	initialize: function(options) {
		this.count = 0;
		this.hasPic = options.hasPic;
		this.viewCollection = new Array();
		$(".main").append(this.render().el);
		this.scrollToLoad()
	},
	render: function() {
		var that = this;
		var length = this.model.length;
		var models = this.model.models;
		for (var i = 0; i < length; i++) {
			if (that.hasPic) {
				var itemview = new app.ItemView({
					model: models[i]
				});
				var $el = $(itemview.render().el);
                                var genre = models[i].get('Goods').genre;
                                var catalogId = models[i].get('Goods').catalog_id;
				if (genre == "3" || catalogId == "1") {
					$el.addClass('large');
					$el.find('.select-shadow').addClass("large")
					$el.find('.soldout-shadow').addClass("large")
				}
				that.viewCollection.push(itemview)
			} else {
				var itemview = new app.ItemViewWithoutImg({
					model: models[i]
				});
				var $el = $(itemview.render().el);
                                var genre = models[i].get('Goods').genre;
                                var catalogId = models[i].get('Goods').catalog_id;
				if (genre == "3" || catalogId == "1") {
					$el.addClass('large');
					$el.find('.select-shadow-no-img').addClass("large")
					$el.find('.soldout-shadow-no-img').addClass("large")
				}
				that.viewCollection.push(itemview)
			}
			that.$el.append($el)
		}
		return this
	},
	scrollToLoad: function() {
		var that = this;
		var winHeight = $(window).height(),
			headerHeight = $('#menu-container').find('.header').height();
		marqueeHeight = $('#menu-container').find('.marquee').height();
		footerHeight = $('#menu-container').find('.toolbar').height();
		listInViewHeight = winHeight - headerHeight - footerHeight;
		var bigCount = 0, displayCount = 0;
		var anchor = marqueeHeight;
		for (var i = 0; i < this.viewCollection.length; i++) {
			if (this.viewCollection[i].$el.hasClass('large')) {
				bigCount += 1
			} else {
				break
			}
		};
		while (true) {
			if (bigCount > 0) {
				anchor += (246 + 20);
				bigCount--;
				displayCount++
			} else {
				anchor += (200 + 20);
				displayCount += 2
			}
			if (anchor > listInViewHeight) {
				break
			}
		}
		for (var i = 0; i < displayCount; i++) {
                    if(typeof(this.viewCollection[i]) != "undefined"){
			this.viewCollection[i].imgLazyLoad()
                    }
		};
		$(window).scroll(function() {
			for (var i = displayCount; i < that.viewCollection.length; i++) {
				var height = that.viewCollection[i].$el.height();
				var loadNum = 1;
				if (height == 200) {
					loadNum = 2
				}
				if ($(window).scrollTop() + listInViewHeight >= that.viewCollection[i].$el.offset().top + 51) {
					if (loadNum == 1) {
						that.viewCollection[i].imgLazyLoad();
						displayCount++
					} else if (loadNum == 2) {
						that.viewCollection[i++].imgLazyLoad();
						displayCount++;
						if (that.viewCollection[i]) {
							that.viewCollection[i].imgLazyLoad();
							displayCount++
						}
					}
				}
			}
		})
	}
});

app.ShoppingCartView = Backbone.View.extend({
    template: _.template($("#shoppingCart-template").html()),
    events: {
        'click': 'enterShoppingCart'
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this
    },
    enterShoppingCart: function() {
        if(tradeTime && tradeTime['TradeTime']){
            var nowtime = parseInt(getHHmmss());
            if(nowtime < parseInt(tradeTime['TradeTime'].start_time) || nowtime > parseInt(tradeTime['TradeTime'].end_time)) {
                var popup = new app.OrderInfoPopupView({
                    msg: tradeTime['TradeTime'].tips
                });
                this.$el.append(popup.render().el)
                return false;
            }
        }
        $('.container').css('display', 'none');
        var orderContainer = $('#order-container');
        if (orderContainer.length > 0) {
                orderContainer.remove();
        }
        var orderContainer = new app.OrderView({
                model: this.model
        });
    }
});
var app = app || {};
app.MenuView = Backbone.View.extend({
	className: 'container',
	id: 'menu-container',
	template: _.template($("#menuView-template").html()),
        events: function(){
            var self = this;
            this.$(".menuItem").click(function(){
                var item = $(this);
                var catalogId = item.attr('id').substring(1);
                $('.types ul li').removeClass('active');
		item.addClass('active');
		$('.items').hide();
		$(window).scrollTop(0);
		if ($('#items-' + catalogId).length > 0) {
                    $('#items-' + catalogId).show();
		} else {
                    self.renderList(catalogId);
		}
            });
            this.$("#more-types").click(function(){
                self.toggleDropdown();
            });
            return {};
        },
	hasPic: false,
	initialize: function() {
            $(".main-container").append(this.render().el);
            sc.dropdown("menu-container", ".user");
            sc.togglePic(".togglePic");
	},
	render: function() {
            this.$el.html(this.template({
                slctidx: slctidx,
                catalogs: catalogs,
                moreCatalogs: moreCatalogs
            }));
            // this.$("#m"+catalogs[1].Catalog.id).addClass("active");
            this.$("#m"+catalogs[slctidx].Catalog.id).addClass("active");
            return this;
	},
	setPic: function(hasPic) {
            this.hasPic = hasPic;
	},
        toggleDropdown : function() {
            sc.toggleTypesDropdown();
        },
	renderList: function(kind) {
		var list = items[kind];
		if (list) {
			var currentCollection = new app.ItemCollection();
			var mainId;
			for (var i = 0; i < list.length; i++) {
                                var item = new app.Item(list[i]);
                                item.set('date', getDeliveryDate(item, kind));
                                currentCollection.add(item)
				mainId = "items-" + kind
			}
                        var itemListView = new app.ItemListView({
                                model: currentCollection,
                                id: mainId,
                                hasPic: this.hasPic
                        });
		} else {
			return
		}
		function getDeliveryDate(item, kind) {
			var timestamp;
			var dayArr = ['零', '一', '二', '三', '四', '五', '六', '日'];
                        timestamp = new Date();
                        var nextTimestamp = new Date(timestamp.getTime() + 86400000);
                        var month = nextTimestamp.getMonth() + 1,
                                date = nextTimestamp.getDate(),
                                day = nextTimestamp.getDay();
                        return month + "月" + date + "日"
		}
	},
	handleJSON: function(data, kind) {
		if (data == undefined) {
			var emptyCollection = new app.ItemCollection();
			var emptyListView = new app.ItemListView({
				model: emptyCollection
			});
			return;
		}
		var currentCollection = new app.ItemCollection();
		var mainId;
		for (var i = 0; i < data.length; i++) {
                        var item = new app.Item(data[i]);
                        item.set('date', getDeliveryDate(item, "0"));
                        app.vegetableCollection.add(item);
                        mainId = "items-" + kind;
                        currentCollection = app.vegetableCollection
		}
                var itemListView = new app.ItemListView({
                        model: currentCollection,
                        id: mainId,
                        hasPic: this.hasPic
                })
		function getDeliveryDate(item, kind) {
			var timestamp;
			var dayArr = ['零', '一', '二', '三', '四', '五', '六', '日'];
                        timestamp = new Date();
                        var nextTimestamp = new Date(timestamp.getTime() + 86400000);
                        var month = nextTimestamp.getMonth() + 1,
                                date = nextTimestamp.getDate(),
                                day = nextTimestamp.getDay();
                        return month + "月" + date + "日"

		}
	}
});
app.OrderItemView = Backbone.View.extend({
	tagName: 'li',
	template: _.template($("#orderItemView-template").html()),
	events: {
		'click .minus': 'minus',
		'click .add': 'add',
		'click .delete-btn': 'removeItem'
	},
	initialize: function() {
		if (!this.model.get('count')) {
			this.model.set('count', 1);
			this.model.set('total', parseFloat(this.model.get('Goods').price))
		}
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
                total = parseInt(this.model.get('Goods').total);
		if (this.model.get('count') + 1 <= total) {
	            this.$el.find('.add').removeClass('disabled')
                }

		if (this.model.get('count') > 1) {
			this.$el.find('.minus').removeClass('disabled')
		}
		return this
	},
	minus: function() {
		var count = parseFloat(this.$el.find('.amount').val());

		if (count > 2) {
			this.$el.find('.amount').val(count - 1);
			this.$el.find('.minus').removeClass('disabled')
		} else if (count == 2) {
			this.$el.find('.amount').val(count - 1);
			this.$el.find('.minus').addClass('disabled')
		} else {
			this.$el.find('.minus').addClass('disabled');
			return
		}
		this.model.set('count', count - 1);

                var total = parseInt(this.model.get('Goods').total);
		if (count > total) {
			this.$el.find('.add').addClass('disabled')
		} else {
	            this.$el.find('.add').removeClass('disabled')
                }

		this.model.set('total', (parseFloat(this.model.get('total')) - parseFloat(this.model.get('Goods').price)).toFixed(2));
		app.shoppingCart.set('item_count', app.shoppingCart.get('item_count') - 1);
		app.shoppingCart.set('item_total', (parseFloat(app.shoppingCart.get('item_total')) - parseFloat(this.model.get('Goods').price)).toFixed(2));
		this.updateView(-1)
	},
	add: function() {
		var count = parseFloat(this.$el.find('.amount').val());

                var total = parseInt(this.model.get('Goods').total);
		if (count + 1 < total) {
		        this.$el.find('.amount').val(count + 1);
	                this.$el.find('.add').removeClass('disabled')
		} else if (count + 1 == total) {
		        this.$el.find('.amount').val(count + 1);
			this.$el.find('.add').addClass('disabled')
                } else {
			this.$el.find('.add').addClass('disabled')
                        return 
                }

		if (count + 1 > 0) {
			this.$el.find('.minus').removeClass('disabled')
		} else {
			this.$el.find('.minus').addClass('disabled')
		}
		this.model.set('count', count + 1);
		this.model.set('total', (parseFloat(this.model.get('total')) + parseFloat(this.model.get('Goods').price)).toFixed(2));
		app.shoppingCart.set('item_count', app.shoppingCart.get('item_count') + 1);
		app.shoppingCart.set('item_total', (parseFloat(app.shoppingCart.get('item_total')) + parseFloat(this.model.get('Goods').price)).toFixed(2));
		this.updateView(1)
	},
	removeItem: function() {
		var cid = this.model.get('Goods').id;
		if ($('#item-' + cid).find('.select-shadow').length > 0) {
			$('#item-' + cid).find('.select-shadow').css('display', 'none')
		}
		if ($('#item-' + cid).find('.select-shadow-no-img').length > 0) {
			$('#item-' + cid).find('.select-shadow-no-img').css('display', 'none')
		}
		app.shoppingCart.get('items').remove(this.model);
		this.remove();
		if (app.shoppingCart.get('count') == 0) {
			$('#order-container').hide();
			$('#menu-container').show()
		}
	},
	updateView: function(inc) {
		this.$el.find('.item-amount').html(this.model.get('count'));
		this.$el.find('.item-total-price').html('￥' + this.model.get('total'))
	}
});

app.OrderView = Backbone.View.extend({
	className: 'container',
	id: 'order-container',
	template: _.template($("#orderView-template").html()),
	events: {
		'click .back': 'back',
		'click .next': 'next'
	},
	initialize: function() {
		$(window).scrollTop(0);
		$(".main-container").append(this.render().el);
		sc.dropdown('order-container', ".user")
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		var that = this;
		var items = this.model.get('items');
		items.forEach(function(item) {
			var orderItemView = new app.OrderItemView({
				model: item
			});
			that.$el.find('#item-list').find('ul').append(orderItemView.render().el)
		});
		if (items.length == 0) {
			this.$el.find('#item-list').css('display', 'none')
		}
		return this;
	},
	back: function() {
		this.$el.css('display', 'none');
		$('#menu-container').css('display', 'block')
	},
	next: function() {
		this.$el.css('display', 'none');
		var deliveryContainer = $('#delivery-container');
		if (deliveryContainer.length > 0) {
			deliveryContainer.css('display', 'block')
		} else {
			app.UserInfo = new app.User();
			var deliveryContainer = new app.DeliveryView({
				model: app.UserInfo
			})
		}
	}
});
app.OrderInfoPopupView = Backbone.View.extend({
	className: 'popup',
	id: 'orderInfo-popup',
	template: _.template($("#orderInfoPopupView-template").html()),
	events: {
		'click button': 'close'
	},
	initialize: function(options) {
		this.msg = options.msg
	},
	render: function() {
		this.$el.html(this.template());
		this.$el.find('.popup-header').append(this.msg);
		var that = this;
		setTimeout(function() {
			that.close()
		}, 2000);
		return this
	},
	close: function() {
		this.$el.remove()
	}
});
app.OrderConfirmPopupView = Backbone.View.extend({
	className: 'popup',
	id: 'orderConfirm-popup',
	template: _.template($("#orderConfirmPopupView-template").html()),
	events: {
		'click #yes': 'submit',
		'click #no': 'close',
	},
	initialize: function(options, ajaxSetting) {
		if (options != undefined) {
			if (options.msg) this.msg = options.msg;
			if (options.tips) this.tips = options.tips;
			if (options.yesLabel) this.yesLabel = options.yesLabel;
			if (options.noLabel) this.noLabel = options.noLabel
		}
		if (ajaxSetting != undefined) {
			this.ajaxSetting = ajaxSetting
		}
	},
	render: function() {
		this.$el.html(this.template());
		if (this.msg) this.$el.find('.popup-header').append(this.msg);
		if (this.tips) this.$el.find('.popup-tips').append(this.tips);
		if (this.yesLabel) this.$el.find('#yes').html(this.yesLabel);
		if (this.noLabel) this.$el.find('#no').html(this.noLabel);
		return this
	},
	submit: function() {
		var that = this;
		$.ajax(that.ajaxSetting);
		this.$el.remove()
	},
	close: function() {
		this.$el.remove()
	}
});
app.PaymentView = Backbone.View.extend({
	className: 'payment',
	template: _.template($("#paymentView-template").html()),
	events: {
            'click #balance-payment': 'selectBalance',
            'click #wechat-payment': 'selectWechat',
            'click #alipay-payment': 'selectAlipay',
            'click #cool-payment': 'selectCool'
	},
	initialize: function() {
            app.payType = 2;
        },
	render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            if(cust != null) {
                if(cust.Customer.city != null) {
                    this.$el.find('#hat_city').val(cust.Customer.city);
                }
                if(cust.Customer.area != null) {
                    this.$el.find('#hat_area').val(cust.Customer.area);
                }
            }
            return this;
	},
        getWechatId: function() {
            return (function() {
                var arrStr = document.cookie.split("; ");
                for (var i = 0; i < arrStr.length; i++) {
                    var temp = arrStr[i].split("=");
                    if (temp[0] == 'wechat_id') return unescape(temp[1])
                }
            })()
        },
        selectBalance: function() {
            if(cust == null || parseFloat(cust.Customer.money) < parseFloat(app.shoppingCart.get('item_total'))) {
                var pop = new app.OrderInfoPopupView({
                    msg: '余额不足，请先充值或选择其方式付款'
                });
                this.$el.append(pop.render().el);
                return false;
            }
            this.$el.find('.radio').removeClass('selected');
            this.$el.find('#balance-payment > .radio').addClass('selected');
            app.payType = 3;
	},
        selectWechat: function() {
            var pop = new app.OrderInfoPopupView({
                msg: '正在建设即将开放'
            });
            this.$el.append(pop.render().el);
            return false;
//            this.$el.find('.radio').removeClass('selected');
//            this.$el.find('#balance-payment > .radio').addClass('selected');
//            app.payType = 4;
	},
	selectAlipay: function() {
            this.$el.find('.radio').removeClass('selected');
            this.$el.find('#alipay-payment > .radio').addClass('selected');
            app.payType = 1;
	},
	selectCool: function() {
            this.$el.find('.radio').removeClass('selected');
            this.$el.find('#cool-payment > .radio').addClass('selected');
            app.payType = 2;
	}
});
app.DeliveryView = Backbone.View.extend({
    className: 'container',
    id: 'delivery-container',
    template: _.template($("#deliveryView-template").html()),
    areaItemTemplate: _.template('<% _.each(areas, function(item, idx) { %> <option value="<%= item.Address.id %>"><%= item.Address.name %></option> <% }); %>'),
    events: {
        'click .back': 'back',
        'click .next': 'next',
        'change #hat_city': 'renderHatArea'
    },
    initialize: function() {
        $(window).scrollTop(0);
        $(".main-container").append(this.render().el);
        var payment = new app.Payment();
        var paymentView = new app.PaymentView({
            model: payment
        });
        this.$el.find('.confirmation-form').after(paymentView.render().el);
        sc.dropdown('delivery-container', ".user")
    },
    render: function() {
        this.$el.html(this.template({
            cities: cities, 
            areas: areas[cities[0].Address.id],
            deliveryTimes: deliveryTimes,
            organization: organization
        }));
        this.$el.find("#hat_city").val(cust.Customer.city);
        this.$el.find("#hat_area").val(cust.Customer.area);
        return this;
    },
    renderHatArea: function(){
        var cityId = this.$("#hat_city").val();
        this.$("#hat_area").html(this.areaItemTemplate({areas: areas[cityId]}));
    },
    back: function() {
        this.$el.css('display', 'none');
        $('#order-container').css('display', 'block')
    },
    next: function() {
        var that = this;
        var pass = true;
        if (this.userInfoChanged) {
            pass = this.updateUserInfo()
        }
        if (current_user == sc.getWechatId()) {
            if (pass) {
                $('#submitOrderBtn').click(function(){
                    alert("Re submit...");
                });
                var postData = this.extractData();
                $.ajax({
                    url: baseUrl + 'orders/add/' + new Date().getTime(),
                    type: 'post',
                    data: postData,
                    async: false,
                    success: function(data) {
                        var data = eval("(" + data + ")");
                        that.$el.css('display', 'none');
                        if (data.data.cart_id) {
                            app.shoppingCart.set('cart_id', data.data.cart_id);
                            app.shoppingCart.set('amount', data.data.amount);
                            app.shoppingCart.set('status', data.data.status);
                            app.shoppingCart.set('pay_mode', data.data.pay_mode);
                        } else {
                            app.shoppingCart.set('cart_id', "")
                            app.shoppingCart.set('amount', "");
                            app.shoppingCart.set('status', "");
                            app.shoppingCart.set('pay_mode', "");
                        }
                        var orderResultView = new app.OrderResultView({
                            model: app.shoppingCart
                        })
                    },
                    error: function(data) {
                        console.log(data)
                    }
                })
            }
        } else if (current_user && user_status == "NEW_USER") {
            that.$el.hide();
            app.registerView = new app.RegisterView({
                    backTo: "delivery-container"
            })
        } else if (current_user && user_status == "CUSTOMER") {
            that.$el.hide();
            app.loginView = new app.LoginView({
                    backTo: "delivery-container"
            })
        } else if (current_user == undefined) {
            var pop = new app.OrderInfoPopupView({
                    msg: '错误的用户，请重新关注爱好食^_^'
            });
            that.$el.append(pop.render().el)
        }
    },
    updateUserInfo: function() {
        var that = this;
        var telPattern = /^1[3|4|5|8][0-9]{9}$/;
        var tel = that.$el.find('input[name=tel]').val(),
            username = that.$el.find('input[name=username]').val(),
            address = that.$el.find('input[name=address]').val();
        if (telPattern.exec(tel) && username != "" && address != "") {
            $.ajax({
                url: baseUrl + 'customers/edit/' + this.getUuid(),
                type: 'post',
                data: {
                    'Customer': {
                        'open_id': that.getWechatId(),
                        'name': that.$el.find('input[name=username]').val(),
                        'phone': that.$el.find('input[name=tel]').val(),
                        'city': that.$el.find('#hat_city').val(),
                        'area': that.$el.find('#hat_area').val(),
                        'address': that.$el.find('#address').val(),
                        'remark': that.$el.find('input[name=note]').val()
                    }
                },
                success: function(data) {
                    that.userInfoChanged = true;
                },
                error: function() {
                    console.log('error');
                }
            });
            return true;
        } else if (username == "") {
            that.$el.find('input[name=username]').css('color', 'red');
            that.$el.find('input[name=username]').focus();
            that.$el.find('input[name=username]').bind('change', function() {
                $(this).css('color', 'black');
                $(this).unbind('change');
            });
            return false;
        } else if (!telPattern.exec(tel)) {
            that.$el.find('input[name=tel]').css('color', 'red');
            that.$el.find('input[name=tel]').focus();
            that.$el.find('input[name=tel]').bind('change', function() {
                $(this).css('color', 'black');
                $(this).unbind('change');
            });
            return false;
        } else if (address == "") {
            that.$el.find('input[name=address]').css('color', 'red');
            that.$el.find('input[name=address]').focus();
            that.$el.find('input[name=address]').bind('change', function() {
                $(this).css('color', 'black');
                $(this).unbind('change');
            });
            return false;
        }
    },
    getUuid: function() {
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
    },
    getWechatId: function() {
        return (function() {
            var arrStr = document.cookie.split("; ");
            for (var i = 0; i < arrStr.length; i++) {
                var temp = arrStr[i].split("=");
                if (temp[0] == 'wechat_id') return unescape(temp[1])
            }
        })()
    },
    userInfoChanged: function() {
        return true;
    },
    extractData: function() {
        var order = app.shoppingCart;
        var data = {
                Cart: []
        };
        data.payType = app.payType;
        data.deliveryTime = this.$el.find("#deliveryTime").val();
        app.shoppingCart.set('deliveryTime', data.deliveryTime);
        order.get('items').forEach(function(item) {
            var arr = {};
            arr.goods_id = item.get('Goods').id;
            arr.count = item.get('count');
            data.Cart.push(arr)
        });
        data.open_id = this.getWechatId();
        data.name = this.$el.find('input[name=username]').val();
        data.phone = this.$el.find('input[name=tel]').val();
        data.city = this.$el.find('#hat_city').val();
        data.area = this.$el.find('#hat_area').val();
        data.address = this.$el.find('#address').val();
        data.remark = this.$el.find('input[name=note]').val();
        return data;
    }
});

app.OrderResultView = Backbone.View.extend({
    className: 'container',
    id: 'orderResult-container',
    template: _.template($("#orderResultView-template").html()),
    events: {
        'click .next': 'nextOrder'
    },
    initialize: function(options) {
        $(window).scrollTop(0);
        $(".main-container").append(this.render().el);
        sc.dropdown('orderResult-container', ".user");
        var date = new Date();
        $(".date").html((date.getMonth() + 1) + "月" + date.getDate() + "日 " + date.getHours() + ":" + date.getMinutes())
    },
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        var that = this;
        var items = this.model.get('items');
        if (items.length > 0) {
            var itemsList = new app.ItemsResultView({
                model: this.model
            });
            that.$el.find(".orderResultList-container").append(itemsList.render().el);
            items.forEach(function(item) {
                var resultItemView = new app.ResultItemView({
                        model: item
                });
                that.$el.find('#item-order-list').find('ul').append(resultItemView.render().el)
            });
            if(app.shoppingCart.get('pay_mode') == 1) {
                that.$el.find("#pBox").html("付款完成后");
            }
            var dTime = app.shoppingCart.get("deliveryTime");
            for(idx in deliveryTimes){
                if(deliveryTimes[idx].DeliveryTime.id == dTime){
                    //that.$el.find("#timeBox").html(deliveryTimes[idx].DeliveryTime.start_time + "-" + deliveryTimes[idx].DeliveryTime.end_time);
                    that.$el.find("#timeBox").html(organization.Organization.tip_content);
                    break;
                }
            }
        }
        if (items.length == 0) {
                this.$el.find('#items-order-result').css('display', 'none')
        }
        return this;
    },
    nextOrder: function() {
        if(app.shoppingCart.get('pay_mode') == 1) {
            this.$el.find('#alipayForm').submit();
        }else{
            window.location.reload()
        }
    }
});

app.ItemsResultView = Backbone.View.extend({
	template: _.template($('#itemsResultView-template').html()),
	events: {
		'click .cancelOrder': 'cancelOrder'
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		return this;
	},
	cancelOrder: function() {
		var that = this;
		var cart_id = this.model.get('cart_id');
		var confirm = new app.OrderConfirmPopupView({
			msg: '确定取消订单吗？'
		}, {
			url: baseUrl + 'orders/delete/' + cart_id,
			method: 'post',
			success: function(data) {
				console.log(data);
				var data = eval('(' + data + ')');
				if (data.code == 1) {
					var popup = new app.OrderInfoPopupView({
						msg: data.msg
					});
					$('#orderResult-container').append(popup.render().el)
				} else {
					if (data.msg == "订单删除成功") {
						var popup = new app.OrderInfoPopupView({
							msg: data.msg
						});
						$('#orderResult-container').append(popup.render().el);
						that.$el.remove()
					} else {
						var popup = new app.OrderInfoPopupView({
							msg: data.msg
						});
						$('#orderResult-container').append(popup.render().el)
					}
				}
			},
			error: function(data) {
				console.log(data)
			}
		});
		$('#orderResult-container').append(confirm.render().el)
	}
});
app.ResultItemView = Backbone.View.extend({
	tagName: 'li',
	template: _.template($('#resultItemView-template').html()),
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		return this;
	}
});
app.MyOrdersView = Backbone.View.extend({
    className: 'container',
    id: 'myOrders-container',
    template: _.template($("#myOrdersView-template").html()),
    events: {
        'click .next': 'next',
        'click .history-loader': 'loadHistory'
    },
    initialize: function() {
        app.historyPage = 1;
        $(window).scrollTop(0);
        var that = this;
        var now = new Date();
        this.cur_date = parseInt(now.getFullYear() + "" + sc.normalizeNumber(now.getMonth() + 1) + "" + sc.normalizeNumber(now.getDate()));
        this.cur_time = now.getHours();
        $.ajax({
            // today
            url: baseUrl + 'orders/0.json',
            success: function(data) {
                that.rt_data = data.rt_obj.data;
                that.date = data.rt_obj.date;
                that.code = data.rt_obj.code;
                $(".main-container").append(that.render().el);
                sc.dropdown('myOrders-container', '.user');
            },
            error: function() {
                console.log("error");
            }
        })
    },
    render: function() {
        this.$el.html(this.template());
        if (this.code != 2) {
            this.parseOrder();
        }
        return this;
    },
    next: function() {
        window.location.reload()
    },
    loadHistory: function() {
        var that = this;
        //if (this.code != 2) {
            $.ajax({
                // history
                url: baseUrl + 'orders/' + app.historyPage + '.json',
                success: function(data) {
                    that.rt_data = data.rt_obj.data;
                    that.date = data.rt_obj.date;
                    that.code = data.rt_obj.code;
                    if (that.code != 2) {
                        app.historyPage = app.historyPage + 1;
                        that.parseOrder();
                    }
                },
                error: function() {
                    console.log("error");
                }
            })
        //}
    },
    parseOrder: function() {
        if (this.code != 1 && this.code != 2 && this.rt_data.orders) {
            for(var idx in this.rt_data.orders) {
                var oneDayOrderView = new app.OneDayOrderView();
                this.$el.find('.myOrderList').append(oneDayOrderView.render().el);
                
                var ord = this.rt_data.orders[idx].Order;
                var order = new app.Order(ord);
//                var status = " 处理中";
//                var deliver_date = this.getDateStr(this.date, 2);
//                if (this.cur_date > deliver_date) {
//                    status = " 已配送"
//                } else if (this.cur_date == deliver_date) {
//                    if (this.cur_time < 6) {
//                        status = " 采购中"
//                    } else if (this.cur_time >= 6 && this.cur_time < 16) {
//                        status = " 已采购"
//                    } else if (this.cur_time >= 16 && this.cur_time < 19) {
//                        status = " 配送中"
//                    } else if (this.cur_time >= 19) {
//                        status = " 已配送"
//                    }
//                }
                order.set('order_status', ord.order_date + ' 处理中');
                if(ord.delivery_status == 3) {
                    order.set('order_status', ord.order_date + '已完成');
                    ord.status = "已完成";
                }
                else if(ord.delivery_status == 4) {
                    order.set('order_status', ord.order_date + '已结束');
                    ord.status = "已结束";
                }
                order.set('cart_id', ord.id);
                order.set('cart_total', ord.order_money);
                order.set('can_cancel', this.canCancel(ord.pay_mode, ord.status, ord.order_date));
                order.set('status', ord.status);
                order.set('delivery_status', ord.delivery_status);
                order.set('freight', ord.freight);
                var itemOrderView = new app.ItemOrderView({
                    model: order,
                    status: ord.status
                });
                oneDayOrderView.$el.find('.orderResult-form').append(itemOrderView.render().el);
                var items = this.rt_data.orderItems[ord.id];
                for (var i = 0; i < items.length; i++) {
                    var item = new app.OrderGoods(items[i]);
                    var goods = {'goods_name':item.get('OrderGoods').goods_name};
                    item.set('Goods', goods);
                    item.set('count', parseInt(item.get('OrderGoods').goods_num));
                    item.set('total', item.get('count') * parseFloat(item.get('OrderGoods').goods_price));
                    var resultItemView = new app.ResultItemView({
                        model: item
                    });
                    itemOrderView.$el.find('ul').append(resultItemView.render().el);
                }
            }
        }
    }
//    ,getDateStr: function(date, AddDayCount) {
//        date = "" + date;
//        var year = date.substr(0, 4);
//        var month = date.substr(4, 2);
//        var day = date.substr(6, 2);
//        var dd = new Date(year, month, day);
//        dd.setDate(dd.getDate() + AddDayCount);
//        var y = dd.getFullYear();
//        var m = dd.getMonth();
//        if (m < 10) {
//            m = "0" + m
//        }
//        var d = dd.getDate();
//        if (d < 10) {
//            d = "0" + d
//        }
//        return parseInt(y + "" + m + "" + d);
//    }
    ,canCancel: function(payMode, status, orderDate){
        if(this.cur_date > orderDate) {
            return false;
        }
        if(payMode == 2) {
            return true;
        }
        if((payMode == 1 || payMode == 4) && status == 4) {
            return true;
        }
        return false;
    }
});

app.OneDayOrderView = Backbone.View.extend({
    template: _.template($('#oneDayOrderView-template').html()),
    render: function() {
        this.$el.html(this.template());
        return this;
    }
});

app.ItemOrderView = Backbone.View.extend({
	template: _.template($('#itemOrderView-template').html()),
	events: {
		'click .cancelOrder': 'cancelOrder'
	},
	initialize: function(options) {
		if (options != undefined) {
			this.status = options.status
		}
	},
	render: function() {
		this.$el.html(this.template(this.model.toJSON()));
		if (this.status && this.status.trim() == "已配送") {
			this.$el.find('.cancelOrder').remove()
		}
		else if (this.status && this.status.trim() == "已完成") {
			this.$el.find('.cancelOrder').remove()
		}
		return this
	},
	cancelOrder: function() {
		var that = this;
		var cart_id = this.model.get('cart_id');
//		if (that.status.trim() == "处理中" || that.status.trim() == "采购中") {
			var confirm = new app.OrderConfirmPopupView({
				msg: '确定取消订单吗？'
			}, {
				url: baseUrl + 'orders/delete/' + cart_id,
				method: 'post',
				success: function(data) {
					var data = eval('(' + data + ')');
					if (data.code == 1) {
						var popup = new app.OrderInfoPopupView({
							msg: data.msg
						});
						$('#myOrders-container').append(popup.render().el)
					} else {
						if (data.msg == "订单删除成功") {
							var popup = new app.OrderInfoPopupView({
								msg: data.msg
							});
							$('#myOrders-container').append(popup.render().el);
							that.$el.remove()
						} else {
							var popup = new app.OrderInfoPopupView({
								msg: data.msg
							});
							$('#myOrders-container').append(popup.render().el)
						}
					}
				},
				error: function(data) {
					console.log(data)
				}
			});
			$('#myOrders-container').append(confirm.render().el)
//		} else if (that.status.trim() == "已采购") {
//			var confirm = new app.OrderConfirmPopupView({
//				msg: '您的订单我们已采购',
//				tips: '现在取消会造成我们的损失',
//				yesLabel: '取消订单',
//				noLabel: '保留订单'
//			}, {
//				url: baseUrl + 'orders/delete/' + cart_id,
//				method: 'post',
//				success: function(data) {
//					var data = eval('(' + data + ')');
//					if (data.code == 1) {
//						var popup = new app.OrderInfoPopupView({
//							msg: data.msg
//						});
//						$('#myOrders-container').append(popup.render().el)
//					} else {
//						if (data.msg == "订单删除成功") {
//							var popup = new app.OrderInfoPopupView({
//								msg: data.msg
//							});
//							$('#myOrders-container').append(popup.render().el);
//							that.$el.remove()
//						} else {
//							var popup = new app.OrderInfoPopupView({
//								msg: data.msg
//							});
//							$('#myOrders-container').append(popup.render().el)
//						}
//					}
//				},
//				error: function(data) {
//					console.log(data)
//				}
//			});
//			$('#myOrders-container').append(confirm.render().el)
//		} else if (that.status.trim() == "配送中") {
//			var popup = new app.OrderInfoPopupView({
//				msg: '您的订单已经开始配送'
//			});
//			$('#myOrders-container').append(popup.render().el)
//		} else if (that.status.trim() == "已配送") {
//			var popup = new app.OrderInfoPopupView({
//				msg: '订单已经配送成功，不能取消'
//			});
//			$('#myOrders-container').append(popup.render().el)
//		}
	}
});
