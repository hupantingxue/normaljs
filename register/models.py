#-*- coding: utf8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
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
    
    openid = models.CharField(primary_key=True,
                              max_length=100)
    account = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=100,
                            default=u'深圳')
    area = models.CharField(max_length=100)
    addr = models.CharField(max_length=500)
    money = models.FloatField(
        validators = [MinValueValidator(0.0), MaxValueValidator(9999)],
        default = 0.0)
    telphone = models.CharField(max_length=30)
    sex = models.CharField(max_length=6,
                           choices=SEX_CHOICES,
                           default=MALE)
    reg_date = models.DateTimeField('date registered')
