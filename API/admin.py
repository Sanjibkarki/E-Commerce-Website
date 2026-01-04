from django.contrib import admin
from .models import Cart, CartItem, GuestCart
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(GuestCart)

from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
