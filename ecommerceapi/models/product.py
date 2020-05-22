from django.db import models
from django.db.models import F
from .product_type import ProductType
from .customer import Customer

class Product(models.Model):
  
    '''
        Product Models:
        
        Arguments Required:
            title-- character field
            customer-- foreign key for Customer
            price-- decimal field
            description-- character field
            quantity-- integer field
            location-- character field
            image_path-- character field
            created_at-- date-time field
            product_type-- foreign key for ProductType    
    '''
    title = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    ## TODO: Confirm: decimal_places
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField() 
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = (F('created_at').desc(nulls_last=True),)