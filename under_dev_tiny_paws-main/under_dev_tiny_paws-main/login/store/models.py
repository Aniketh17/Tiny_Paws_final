from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.first()

class Category(models.Model):
    name = models.CharField(max_length=100)
    heading = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/', default='products/images/default.jpg')

    def __str__(self):
        return self.name
    
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Ensure quantity is always positive

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'