from django.db import models
from datetime import date
# Create your models here.

class State(models.Model):
    state_name = models.CharField(max_length=50)
    state_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.state_name


class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=64)
    district_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.district_name

class slotrequest(models.Model):
    #name = models.CharField(max_length=64)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,null=True)
    date = models.DateField(default =  date.today,null = False)
    pin = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=254,null = False)
    #verify_mail_sent = models.CharField(max_length = 10,default = 'NO')
    processed = models.CharField(max_length = 10,default = 'NO')
#class ids_s(models.Model):
#    name  = models.CharField(max_length=50)
#    ix = models.IntegerField()


#class ids_d(models.Model):
#    name = models.CharField(max_length=50)
#    ix = models.IntegerField()
