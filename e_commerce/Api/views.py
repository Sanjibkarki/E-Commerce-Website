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
from rest_framework.exceptions import AuthenticationFailed
class api(APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        Order = Ordermodel.objects.all()
        serializer = MyModelSerializer(Order, many=True)
        return Response(serializer.data)
    
    
class Listview(generics.ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated:
            queryset = queryset.filter(product__customer=user,oredered = False)
        return queryset
    
    def list(self,request,*args,**kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            raise AuthenticationFailed('Token not provided')
    
        try:
            token = token.split(' ')[1]
            user = authentication.TokenAuthentication().authenticate_credentials(token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Invalid token')
        cartItem = request.session.get('cart-items', list())
        if cartItem:
            items_to_create = []
            for item in cartItem:
                if 'PName' in item and 'PPrice' in item:
                        cart_item = Ordermodel(
                            product = Customer.objects.get(customer=request.user),
                            PName=item['PName'],
                            PPrice=item['PPrice'],
                            Size=item['Size'],
                            Quantity=item['Quantity'],
                        )
                        items_to_create.append(cart_item)
            if items_to_create:
                cart_item = Ordermodel.objects.bulk_create(items_to_create)
                del request.session['cart-items']
        cart_Item = self.get_queryset()
        serializer = MyModelSerializer(cart_Item, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)


class sessiondata(View):
    def get(self, request):
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
            cart_items = request.session.get('cart-items',list())
            for i in range(len(cart_items)):
                if data.get("PName") == cart_items[i]["PName"]:
                    cart_items[i]["Quantity"] = str(int(data.get("Quantity", 0)) + int(cart_items[i]["Quantity"]))
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
                if cartItem[i]["PName"] == slug:
                    cartItem.pop(i)
                    
            request.session["cart-items"] = cartItem
        return JsonResponse({"Data":"Data Not Available"},safe=False)
        
     
class CreateApi(generics.ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer
    
    def get_queryset(self,*args,**kwargs):
        id = Customer.objects.get(customer = self.request.user)       
        qs = super().get_queryset(*args,**kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return product.objects.none()
        return qs.filter(product = id)
    
    def perform_create(self,serializer):
        id = Customer.objects.get(customer = self.request.user)       
        if serializer.is_valid():
            serializer.save(product = id,oredered = True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Token not provided')
    
        try:
            token = token.split(' ')[1]
            user = authentication.TokenAuthentication().authenticate_credentials(token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Invalid token')
        try:
            obj = Ordermodel.objects.filter(product__customer=request.user)
            for i in obj:
                i.oredered = True
                i.save()
            return Response({"Data":"Method Post Done"})
        except Ordermodel.DoesNotExist:
            return Response({'error': f'Object with ID {obj_id} not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    #     return Response({'message': 'Objects updated successfully'}, status=status.HTTP_200_OK)
class AddCartApi(generics.ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ordermodel.objects.all()
    serializer_class = MyModelSerializer
    
    def get_queryset(self,*args,**kwargs):
        id = Customer.objects.get(customer = self.request.user)       
        qs = super().get_queryset(*args,**kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return product.objects.none()
        return qs.filter(product = id).filter(oredered = False)
    
    def perform_create(self,serializer):
        id = Customer.objects.get(customer = self.request.user)       
        if serializer.is_valid():
            serializer.save(product = id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        data = request.data  
        token = request.headers.get('Authorization')
        id,created = Customer.objects.get_or_create(customer = self.request.user)
        if not token:
            raise AuthenticationFailed('Token not provided')
    
        try:
            token = token.split(' ')[1]
            user = authentication.TokenAuthentication().authenticate_credentials(token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Invalid token')
        try:
            matching = Ordermodel.objects.get(PName=data.get("PName"))
            matching.Quantity += int(data.get("Quantity"))
            matching.save()
            return Response({"data": "dsad"})
            
        except Ordermodel.DoesNotExist:            
            serializer = MyModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product = Customer.objects.get(customer = request.user))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

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
            