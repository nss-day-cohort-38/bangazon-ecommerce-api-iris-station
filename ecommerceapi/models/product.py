from django.db import models
from django.db.models import F
from .product_type import ProductType
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Product(SafeDeleteModel):
  
    '''
        Product Models:
        
        Arguments Required:
            title-- character field
            customer-- foreign key for Customer
            price-- decimal field
            description-- character field
            quantity-- integer field
            location-- character field
            image_path-- ImageField
            created_at-- date-time field
            product_type-- foreign key for ProductType    
    '''

    _safedelete_policy = SOFT_DELETE

    title = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField() 
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)
    amount_sold = 0

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = (F('created_at').desc(nulls_last=True),)