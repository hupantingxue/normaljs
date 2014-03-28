var app = app || {};

app.Delivery = Backbone.Model.extend({
	defaults: {
		way: "",
		time: "",
	},

	initialize: function() {
		console.log("A delivery model has been created!");
	}
});

app.Extra = Backbone.Model.extend({
	defaults: {
		transfee: "",
		discounts: ""
	},

	initialize: function() {
		console.log("An extra model has been created!");
	}
});

app.Item = Backbone.Model.extend({
	defaults: {
		id: "",
		count: 0,
		total: 0
	},

	initialize: function() {
		// console.log("a new item has been created!");
		this.set('id', this.get('Goods').id);

		this.on("invalid", function(model, error) {
			console.log(error);
		});
	},

	validate: function(attrs) {

	}
});

app.OrderGoods = Backbone.Model.extend({
    defaults: {
        id: "",
        goods_id: "",
        count: 0,
        total: 0
    },

    initialize: function() {
//        this.set('id', this.get('OrderGoods').id);
        this.set('goods_id', this.get('OrderGoods').goods_id);
//        this.set('count', this.get('OrderGoods').goods_num);
//        this.set('total', (this.get('OrderGoods').goods_num * this.get('OrderGoods').goods_price).toFixed(2));
        this.on("invalid", function(model, error) {
            console.log(error);
        });
    },

    validate: function(attrs) {

    }
});

app.Order = Backbone.Model.extend({
	defaults: {
		id: "",
		time: "",
		count: 0,
		total: 0,
		item_count: 0,
		item_total: 0,
		items: null,
	},

	initialize: function() {
		var that = this;
		var items = new app.ItemCollection();
		this.set('items', items);

		this.on('invalid', function(model, error) {
			console.log(error);
		});

		// 为订单的菜品集合添加add事件监听
		this.get('items').on('add', function(model) {
			model.set('count', 1);
			model.set('total', model.get('Goods').price);
			that.set('item_count', that.get('item_count') + model.get('count'));
			that.set('item_total', (parseFloat(that.get('item_total')) + model.get('count') * parseFloat(model.get('Goods').price)).toFixed(2));
			that.set('count', that.get('item_count'));
			that.set('total', that.get('item_total'));
		});

		// 为订单的菜品集合添加remove事件监听
		this.get('items').on('remove', function(model) {
			that.set('item_count', that.get('item_count') - model.get('count'));
			that.set('item_total', (parseFloat(that.get('item_total')) - model.get('count') * parseFloat(model.get('Goods').price)).toFixed(2));
			that.set('count', that.get('item_count'));
			that.set('total', that.get('item_total'));
		});

		this.on('change:item_count', function() {
			that.set('count', that.get('item_count'));
			// $('.items-total-amount').html(that.get('item_count'));
		});

		this.on('change:item_total', function() {
			that.set('total', that.get('item_total'));
			$('.items-total-price').html(that.get('item_total'));
		});

		// 为订单的菜品数目添加change事件监听
		this.on('change:count', function(data) {
			$('.total-amount').each(function() {
				$(this).html(that.get('count'));
			});

			if (data.get('count') <= 0) {
				app.shoppingCartV.$el.hide();
			} else {
				app.shoppingCartV.$el.show();
			}
		});

		// 为订单的总价格添加change事件监听
		this.on('change:total', function() {
			$('.total-price').each(function() {
				$(this).html(that.get('total'));
			});
		});
	},

	validate: function(attrs) {
		if (typeof attrs.count !== 'number') {
			return "count must be a number";
		} else if (typeof attrs.count === 'number' && attrs.count < 0) {
			return "count can not be less than zero";
		}
	}
});

app.Payment = Backbone.Model.extend({
	defaults: {
		online: {
			name: 'online',
			label: '在线支付',
			status: false
		},

		cool: {
			name: 'cool',
			label: '货到付款',
			status: false
		}
	},

	initialize: function() {
		// console.log("A payment model has been created!");
	}
});

app.User = Backbone.Model.extend({
	defaults: {
		wechatId: "",
		name: "",
		address: "",
		phone: "",
		remark: ""
	},

	initialize: function() {
		// console.log("A user model has been created!");

		this.on("invalid", function(model, error) {
			console.log(error);
		});
	},

	validate: function(attrs) {
		
	}
});

app.Catalog = Backbone.Model.extend({
	defaults: {
		id: "",
		name: ""
	},

	initialize: function() {
		// console.log("a new item has been created!");
		this.set('id', this.get('Catelog').id);

		this.on("invalid", function(model, error) {
			console.log(error);
		});
	},

	validate: function(attrs) {

	}
});

app.ItemCollection = Backbone.Collection.extend({
	model: app.Item,
});

app.CatalogCollection = Backbone.Collection.extend({
	model: app.Catalog,
});
