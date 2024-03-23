from django.shortcuts import render,HttpResponse
from django.views import View
from django.db.models import Q
from itertools import chain
from Home.models import Upperwear,Lowerwear,Footwear
from Posti.models import Ordermodel,Customer,Product
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Api.serializers import MyModelSerializer 
from Posti.form import UploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
import json

class Views(View):
    def get(self,request):
        try:
            if request.user.is_authenticated:
                get_customer = Customer.objects.get(customer = request.user)
        except Customer.DoesNotExist:
            return render(request,"front_pages/view.html")
        return render(request,"front_pages/view.html",{"is_authenticated":request.user.is_authenticated})


def Prod_detail(request,product_slug):
    try:
        product = Upperwear.objects.get(product_name=product_slug)
    except Upperwear.DoesNotExist:
        try:
            product = Lowerwear.objects.get(product_name=product_slug)
        except Lowerwear.DoesNotExist:
            try:
                product = Footwear.objects.get(product_name=product_slug)
            except Footwear.DoesNotExist:
                product = None 
    return render(request,"front_pages/product_detail.html",{"product":product})


    return render(request,'front_pages/add.html',{'form':form})
# def delete(request):
#     c = Customer.objects.get(customer = "sanjibkarki64@gmail.com")
#     # d = c.inlinemodel_set.all()
#     print(c.ordermodel_set.all().delete())
#     return render(request,"base.html")


# Query all models with a single database hit


class prod_search(View):
    def get(self, request,query = None):
        query = request.GET.get('query')
        combined_query = Q(product_name__icontains=query)
        if query is not None:
            
            results = list(chain(
                Upperwear.objects.filter(combined_query),
                Lowerwear.objects.filter(combined_query),
                Footwear.objects.filter(combined_query)
            ))
            if results:
                context = { 'results': results,'query':query}     
                return render(request, 'front_pages/search.html', context)
            else:
                return render(request, 'front_pages/no_match.html')
                    
            
        else: 
            a = list(chain(
                Upperwear.objects.filter(combined_query),
                Lowerwear.objects.filter(combined_query),
                Footwear.objects.filter(combined_query)
            ))[:8]
            results = a[:8]
             
        context = { 'results': results}
        return render(request, 'front_pages/search.html', context)


     
# def prod_search(request,query = None):
#     if request.method == "GET":
#         
#         if prod1 or prod2 or prod3:
#             combined_query = list(chain(prod1, prod2, prod3))
#             return render(request,"front_pages/search.html",{"product":results})
#         else:
#             return HttpResponse("<b><center>No Result Found</center></b>")
#     return HttpResponse("hello")
    
    
    