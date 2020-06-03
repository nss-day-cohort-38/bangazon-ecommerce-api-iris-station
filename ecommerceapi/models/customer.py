from django.db import models
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.models import User


class Customer(models.Model):
    '''
        Customer Model 
        
        Arguments Required:
          user--user 1-1 field
          address-character field
          phone_number-character field
    '''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=55)    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = (F('user__date_joined').asc(nulls_last=True),)