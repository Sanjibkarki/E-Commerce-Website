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
from django.views import View
from django.http import JsonResponse
from Posti.models import Ordermodel,Customer

class api(APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        Order = Ordermodel.objects.all()
        serializer = MyModelSerializer(Order, many=True)
        return Response(serializer.data)
    

class sessiondata(View):
    def get(self, request):
        cartItem = request.session.get('cart-items', list())
        if request.user.is_authenticated:
            if cartItem:
                items_to_create = []
                for item in cartItem:
                    if 'PName' in item and 'PPrice' in item:
                            cart_item = Ordermodel(
                                product = Customer.objects.get(customer=request.user),
                                PName=item['PName'],
                                PPrice=item['PPrice'],
                                Size=item['size'],
                                Quantity=item['quantity'],
                            )
                            items_to_create.append(cart_item)
                if items_to_create:
                    cart_item = Ordermodel.objects.bulk_create(items_to_create)
                    del request.session['cart-items']

            cart_Item = Ordermodel.objects.filter(product__customer = request.user)
            if cart_Item:
                a = []
                for i in cart_Item:
                    a.append({
                        "PName":i.PName,
                        "PPrice":i.PPrice,
                        "size":i.Size,
                        "quantity":i.Quantity
                    })
                cart_Item = a
            else:
                cart_Item = {}
            return JsonResponse({"cartItem":cart_Item},safe = False)
            # return JsonResponse([Ordermodel.objects.filter(product__customer=request.user).values_list()],safe = False)
        
        else:
            try:   
                cartItem = request.session.get('cart-items', list()) 
                data = {
                    'cartItem': cartItem,
                }
            except KeyError:
                data = {
                    'cartItem': list(),

                }

            return JsonResponse(data)
                

    def post(self, request):
        try:
            data = json.loads(request.body)
            customer,created = Customer.objects.get_or_create(customer = request.user)

            if request.user.is_authenticated:
                try:
                    matching = Ordermodel.objects.get(PName=data.get("PName"))
                    matching.Quantity += int(data.get("quantity"))
                    matching.save()
                
                except Ordermodel.DoesNotExist:
                    cart_item = Ordermodel(
                                    product = Customer.objects.get(customer=request.user),
                                    PName=data['PName'],
                                    PPrice=data['PPrice'],
                                    Size=data['size'],
                                    Quantity=data['quantity'],
                                )
                    cart_item.save()
                return JsonResponse({"status": "success", "data": data})
                
            else:
                cart_items = request.session.get('cart-items',list())
                for i in range(len(cart_items)):
                    if data.get("PName") == cart_items[i]["PName"]:
                        cart_items[i]["quantity"] = str(int(data.get("quantity", 0)) + int(cart_items[i]["quantity"]))
                        break
                else:  
                    cart_items.append(data)

                request.session['cart-items'] = cart_items
                return JsonResponse({"status": "success", "data": data})
        except json.JSONDecodeError as e:
            return JsonResponse({"status": "error", "message": str(e)})

        
            
class sessiondata_delete(View):
    def delete(self,request,slug):
        if request.user.is_authenticated:
            try:
                
                cartItem = Ordermodel.objects.filter(product__customer = request.user)
                delete_item = cartItem.get(PName = slug)
                delete_item.delete()
            except Ordermodel.DoesNotExist:
                cartItem = None    
        else:
            cartItem = request.session.get('cart-items',{})
            for i in range(len(cartItem)):
                if i == id:
                    cartItem.pop(i)
            request.session["cart-items"] = cartItem
        return JsonResponse({"Data":"Data Not Available"},safe=False)
        
     
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
            