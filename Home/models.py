from django.db import models
import uuid
from Accounts.models import User

#Customer
class Customer(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.customer)
    
#Products
class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Image = models.FileField(upload_to="image") 
    Name = models.CharField(max_length=50)
    Description = models.TextField(default="This is product description")
    Price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    Quantity = models.IntegerField()
    category = models.CharField(
        max_length=1,
        choices=[
            ('E', 'Electronics'),
            ('F', 'Fashion'),
            ('A', 'Accessories'),
            ('W', 'Wearables'),
            ('C', 'Computers'),
        ]
    )

    def __str__(self):
        return self.Name