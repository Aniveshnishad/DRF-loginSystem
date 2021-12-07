from django.db import models


# Create your models here.
class Banks(models.Model):
    bank_name = models.CharField(max_length=200, blank=True)
    branch_name = models.CharField(max_length=100,blank=True)
    bank_address = models.CharField(max_length=200, blank=True)
    IFSC_code = models.CharField(max_length=11,blank=True)
    class Meta:
        ordering = ['bank_name']
    def __str__(self):
        return self.bank_name
