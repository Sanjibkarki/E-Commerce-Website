from django.db import models
from accounts.models import User
from django.db.models import Q

SIZES = [
    ('XXL', 'Very extra Large'),
    ('XL', 'Extra Large'),
    ('L', 'Large'),
    ('M', 'Medium'),
    ('S', 'Small'),
    
]

class Customer(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.customer)
    
class Ordermodel(models.Model):
    product = models.ForeignKey(Customer,on_delete=models.CASCADE) 
    PName = models.CharField(max_length=50)
    PPrice = models.DecimalField(max_digits=1000,decimal_places=2,default=1.99)
    Size = models.CharField(max_length=5, choices=SIZES)
    Quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True,)
    oredered = models.BooleanField(default = False)
    
class Product(models.Model):
    Image = models.FileField(upload_to="image") 
    PName = models.CharField(max_length=50)
    PPrice = models.DecimalField(max_digits=1000,decimal_places=2,default=1.99)
    Quantity = models.IntegerField()
    category = models.CharField(max_length=50, choices=[('U','Upper'),('L','Lower'),('F','Foot')])

