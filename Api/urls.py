from Api.views import api,RetrieveApi,AddCartApi,sessiondata,Listview,CreateApi,SearchList,sessiondata_delete
from django.urls import path,include

urlpatterns = [
    path('',api.as_view()),
    path('list/',Listview.as_view(),name="list"),
    path('session/',sessiondata.as_view(),name="session"),
    
    path('session_delete/<slug:slug>/',sessiondata_delete.as_view(),name="sessiondelete"),
    path('addcart/',AddCartApi.as_view(),name='addcart'),
    path('create/',CreateApi.as_view(),name='create'),
    path('<int:pk>/',RetrieveApi.as_view(),name='detail'),
    path('search/',SearchList.as_view())
    
]


