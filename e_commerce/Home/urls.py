from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include,re_path
from Home.views import Index
from rest_framework import routers,serializers
from Posti.views import Views,Prod_detail,prod_search
from accounts.views import Login,Signup,Logout
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',Index.as_view(),name="home"),
    path('view/',Views.as_view(),name="view"),
    path('form/',include('add_product.urls')),
    
    path('product_detail/<slug:product_slug>/',Prod_detail,name="product_detail"),
    path('search/',prod_search.as_view(),name="product_search"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_complete_form/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('login/',Login.as_view(),name="login"),
    path('signup/',Signup.as_view(),name="signup"),
    path('logout',Logout.as_view(),name="logout")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
