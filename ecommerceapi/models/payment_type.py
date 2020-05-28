from django.db import models
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
class PaymentType(SafeDeleteModel):
    '''
        Payment Type Model:
        
        Arguments Required:
            merchant_name - CharField
            account_number = CharField
            expiration_date = DateField 
            customer_id = ForeignKey of Customer
            created_at = DateTimeField 
            
    '''
    _safedelete_policy = SOFT_DELETE

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateField() 
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField() 
    
    def __str__(self):
        return f'{self.merchant_name}'