from django.urls import path,include,re_path
from .views import form
urlpatterns = [
    path('',form,name="form"),
    path('add/',form,name="form")
]
