from django.urls import path,include,re_path
from .views import form,viewOrders,manageProduct
urlpatterns = [
    path('',form,name="form"),
    path('order/',viewOrders,name="order"),
    path('manage/',manageProduct,name="manage")
    
]
