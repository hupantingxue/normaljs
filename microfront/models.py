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
