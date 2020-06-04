from django.db import models

class ProductType (models.Model):
  
    '''
        Product Type Model
        
        Arguments Required:
            name -- CharField
    '''
    
    name = models.CharField(max_length=55)
    
    def __str__(self):
        return self.name
