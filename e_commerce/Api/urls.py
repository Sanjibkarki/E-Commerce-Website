from Api.views import api,ListCreateApi,RetrieveApi,SearchList
from django.urls import path,include

urlpatterns = [
    path('',api.as_view()),
    path('create/',ListCreateApi.as_view(),name='create'),
    path('<int:pk>/',RetrieveApi.as_view(),name='detail'),
    path('search/',SearchList.as_view())
    
]
