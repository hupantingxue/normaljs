from django.db import models

# Create your models here.
# menu catalog
class Catalog(models.Model):
    name = models.CharField(max_length=200)
    url  = models.CharField(max_length=200)
    sort = models.IntegerField()
    status = models.IntegerField()
    orgid = models.IntegerField()


