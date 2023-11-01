from django.db import models
SIZES = [
    ('XXL', 'Very extra Large'),
    ('XL', 'Extra Large'),
    ('L', 'Large'),
    ('M', 'Medium'),
    ('S', 'Small'),
    
]

# Create your models here.
class Upperwear(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100,decimal_places=2,default=1.99)
    size = models.CharField(max_length=5, choices=SIZES)
    quatity = models.IntegerField(default = 0)
    image = models.FileField(upload_to='image')
    

class Lowerwear(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100,decimal_places=2,default=1.99)
    size = models.CharField(max_length=5, choices=SIZES)
    quatity = models.IntegerField(default = 0)
    image = models.FileField(upload_to='image')
    
class Footwear(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100,decimal_places=2,default=1.99)
    size = models.CharField(max_length=5, choices=SIZES)
    quatity = models.IntegerField(default = 0)
    image = models.FileField(upload_to='image')

