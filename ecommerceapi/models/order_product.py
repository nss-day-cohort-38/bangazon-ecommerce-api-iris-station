from django.db import models
from .order import Order
from .product import Product

class OrderProduct(models.Model):
  
  '''
    Order Product Model
    
    Arguments Required:
        order= ForeignKey for Order
        product= ForeignKey for Product
          
  '''
  
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)