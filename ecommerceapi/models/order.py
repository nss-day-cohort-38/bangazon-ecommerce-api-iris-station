from django.db import models
from .customer import Customer
from django.db.models import F
from .payment_type import PaymentType

class Order(models.Model):
  
  '''
    Order Model
    
    Arguments Required:
      customer-- ForeignKey for Customer
      payment_type-- ForeignKey for PaymentType
      created_at -- DateTimeField
  '''
  
  customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
  payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, blank=True, null=True)
  created_at = models.DateTimeField()

  class Meta:
        ordering = (F('created_at').desc(nulls_last=True),)