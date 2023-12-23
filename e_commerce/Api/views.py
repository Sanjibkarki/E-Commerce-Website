from django.shortcuts import render,redirect
from Posti.models import Ordermodel,Customer
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import generics,permissions,authentication
from Api.serializers import MyModelSerializer 
from django.contrib.auth.mixins import LoginRequiredMixin
class api(APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        Order = Ordermodel.objects.all()
        serializer = MyModelSerializer(Order, many=True)
        return Response(serializer.data)
    # def post(self,request):
    #     data = JSONParser().parse(request) 
    #     serializer = MyModelSerializer(data= data)
    #     print(serializer.data)
    #     if serializer.is_valid():
    #         print(serializer.data)
    #         serializer.save()

    #         # Return a success response
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         # Return an error response with validation errors
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListCreateApi(generics.ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer
    
    def perform_create(self,serializer):
        id = Customer.objects.get(customer = self.request.user)       
        if serializer.is_valid():
            serializer.save(product = id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get_queryset(self,*args,**kwargs):
        id = Customer.objects.get(customer = self.request.user)       
        qs = super().get_queryset(*args,**kwargs)
        print(qs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return product.objects.none()
        return qs.filter(product = id)
    
class RetrieveApi(generics.RetrieveAPIView):
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer 

class SearchList(generics.ListAPIView):
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer
    
    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        
        q = self.request.GET.get('q')
        results = Ordermodel.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q,user=user)
        return results
            