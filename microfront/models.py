#-*- coding:utf8 -*-

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce.models import HTMLField

# Create your models here.
class Menu(models.Model):
    name = models.CharField(unique=True, max_length=100)
    orgid = models.IntegerField()
    catalog_id = models.IntegerField()
    cover_url= models.CharField(max_length=200)
    detail_url = models.CharField(max_length=200)
    old_price = models.FloatField(
        validators = [MinValueValidator(0.0), MaxValueValidator(9999)],
        default = 0.0)
    price = models.FloatField(
        validators = [MinValueValidator(0.0), MaxValueValidator(9999)],
        default = 0.0)
    total = models.IntegerField(null=True) #total amount
    sales = models.IntegerField(null=True, default=0) #sale amount
    genre = models.IntegerField(null=True, default=0)
    level = models.IntegerField(null=True, default=0)
    introduce = HTMLField(verbose_name='detail context',max_length=200000, blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    servings = models.IntegerField(null=True, default=0)
    commodity = models.CharField(max_length=500, null=True, default=u'无')
    zan_num = models.IntegerField(null=True, default=0)

# menu catalog
class Catalog(models.Model):
    name = models.CharField(max_length=200)
    url  = models.CharField(max_length=200, default='url', blank=True)
    sort = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    orgid = models.IntegerField(default=1)

class Order(models.Model):
    price = models.FloatField(
        validators = [MinValueValidator(0.0), MaxValueValidator(9999)],
        default = 0.0)
    openid = models.CharField(max_length=100)
    remark = models.CharField(max_length=500)
    pay_type = models.IntegerField()
    delivery_time = models.IntegerField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=500)
    name = models.CharField(max_length=30)
    delivery_status = models.IntegerField(default=0)
    order_time = models.DateTimeField('order time', default='0000-00-00 00:00:00')
    pay_status = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    shoplist = models.CharField(max_length=1000, null=True, default='')
    order_status = models.CharField(max_length=100, null=True, default=u'已下单，未支付，未配送')

# customer uid
class Customer(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    SEX_CHOICES = (
        (MALE, u'男'),
        (FEMALE, u'女'),
        (UNKNOWN, u'未知'),
    )

    openid = models.CharField(unique=True,
                              max_length=100)
    account = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    city = models.CharField(null=True, max_length=100,
                            default=u'深圳')
    area = models.CharField(null=True, max_length=100)
    addr = models.CharField(null=True, max_length=500)
    money = models.FloatField(null=True, 
        validators = [MinValueValidator(0.0), MaxValueValidator(9999)],
        default = 0.0)
    telphone = models.CharField(max_length=30)
    sex = models.CharField(null=True, max_length=6,
                           choices=SEX_CHOICES,
                           default=MALE)
    reg_date = models.DateTimeField('date registered', default='0000-00-00 00:00:00')
    modify_date = models.DateTimeField('date modified', default='0000-00-00 00:00:00')

# delivery time
class Dltime(models.Model):
    begin_time = models.CharField(max_length=50, null=True, default='00:00:00');
    end_time = models.CharField(max_length=50, null=True, default='00:00:00');

# delivery address
class Dladdr(models.Model):
    province = models.IntegerField(null=True, default=0)
    city = models.IntegerField(null=True, default=0)
    area = models.CharField(max_length=500, null=True, default='');

# other set
class Otherset(models.Model):    
    dx_mobile = models.CharField(max_length=20, null=True, default='15889613776');
    kf_phone = models.CharField(max_length=20, null=True, default='0755-88889999');
    tip_content = models.CharField(max_length=500, null=True, default='');
    distribution_range = models.CharField(max_length=500, null=True, default='');
    freight = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(9999)], default = 0.0)

class Ingredient(models.Model):
    UNIT_KE = 1
    UNIT_BAO = 2
    UNIT_GE = 3
    UNIT_LI = 4
    UNIT_CHOICES = (
        (UNIT_KE, u'克'), 
        (UNIT_BAO, u'包'), 
        (UNIT_GE, u'个'), 
        (UNIT_LI, u'粒'),)
    CLASS_ZHU = 1
    CLASS_FU = 2
    CLASS_CHOICES = ((CLASS_ZHU, u'主料'), (CLASS_FU, u'辅料'),)
    menu_id = models.IntegerField()
    menu_name = models.CharField(max_length=100, null=True, default = '')
    name = models.CharField(max_length=200)
    mclass = models.IntegerField(choices=CLASS_CHOICES, default=CLASS_ZHU) #1: Ingredient  2: accessorie
    quantity = models.IntegerField(default=1)
    unit = models.IntegerField(choices=UNIT_CHOICES, default=UNIT_KE)
