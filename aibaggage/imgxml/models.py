from django.db import models


class NewBaggages(models.Model):
    time = models.DateTimeField(blank = True,null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    imgname = models.CharField(max_length=100)
    objname = models.CharField(max_length=50)
    xmaxi = models.IntegerField(blank=True, null=True)
    ymaxi = models.IntegerField(blank=True, null=True)
    xmini = models.IntegerField(blank=True, null=True)
    ymini = models.IntegerField(blank=True, null=True)