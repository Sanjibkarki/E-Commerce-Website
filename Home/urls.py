from django.urls import path,include
from django.conf import settings
from Home.views import Index, CartView, AdminOrders, AdminOrderDetail, product_search, AddProductView
from django.conf.urls.static import static


urlpatterns = [
    path('',Index.as_view(),name="home"),
    path('view', CartView.as_view(), name='cart'),
    path('form', AddProductView.as_view(), name='add_product'),
    path('orders', AdminOrders.as_view(), name='admin-orders'),
    path('search', product_search, name='product_search'),
    path('orders/<int:pk>/', AdminOrderDetail.as_view(), name='admin-order-detail'),
    path('accounts/',include('Accounts.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
