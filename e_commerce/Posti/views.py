from django.shortcuts import render,HttpResponse
from django.views import View
from Home.models import Upperwear,Lowerwear,Footwear
from Posti.models import Ordermodel,Customer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Posti.serializers import MyModelSerializer 

@csrf_exempt
def my_model_view(request):
    if request.method == 'POST': 
        print(request)
        data = JSONParser().parse(request)     
        serializer = MyModelSerializer(data = data)
        print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Thi isd")
        return HttpResponse("This is it")
    return HttpResponse("This is go")
class Views(View):
    def get(self,request):
        get_customer = Customer.objects.get(customer = request.user)
        return render(request,"front_pages/view.html",{'id':get_customer.id})

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

