from django.urls import path
from .views import (
    ListCreateProductView,
    RetrieveUpdateDestroyProductView,
    CartDetail,
    AddCartItem,
    CartItemDetail,
    AdminOrderList,
    OrderCreate,
)

urlpatterns = [
    path('products/', ListCreateProductView.as_view(), name='product-list'),
    path('products/<uuid:uuid>/', RetrieveUpdateDestroyProductView.as_view(), name='product-detail'),

    # Cart endpoints
    path('cart/', CartDetail.as_view(), name='cart-detail'),
    path('cart/items/', AddCartItem.as_view(), name='cart-add-item'),
    path('cart/items/<int:pk>/', CartItemDetail.as_view(), name='cart-item-detail'),
    # Admin orders
    path('orders/', AdminOrderList.as_view(), name='admin-order-list'),
    path('orders/create/', OrderCreate.as_view(), name='order-create'),
]
