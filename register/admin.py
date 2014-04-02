from django.contrib import admin
from register.models import Customer 

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['openid']}), 
        ('reg information', {'fields':['name', 'reg_date'], 'classes': ['collapse']})]
    list_display = ('openid', 'name', 'reg_date')

admin.site.register(Customer, CustomerAdmin)
