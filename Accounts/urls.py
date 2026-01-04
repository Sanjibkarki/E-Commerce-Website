from .views import Login,Signup,Logout
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login/',Login.as_view(),name="login"),
    path('signup/',Signup.as_view(),name="signup"),
    path('logout',Logout.as_view(),name="logout")
]