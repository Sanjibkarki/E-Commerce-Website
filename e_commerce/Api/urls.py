from Api.views import api,ListCreateApi,RetrieveApi,SearchList,sessiondata,sessiondata_delete
from django.urls import path,include

urlpatterns = [
    path('',api.as_view()),
    path('session/',sessiondata.as_view(),name="session"),
    path('session_delete/<slug:slug>/',sessiondata_delete.as_view(),name="sessiondelete"),
    
    path('create/',ListCreateApi.as_view(),name='create'),
    path('<int:pk>/',RetrieveApi.as_view(),name='detail'),
    path('search/',SearchList.as_view())
    
]
# class sessiondata(View):
#     def get(self, request):
#         try:
#             cartItem = request.session.get('cart-items', list())
#             data = {
#                 'cartItem': cartItem,
                
#             }
#         except KeyError:
#             data = {
#                 'cartItem': list(),
            
#             }
        
#         return JsonResponse(data)
# def post(self, request):
#         try:
#             data = json.loads(request.body)
#             cart_items = request.session.get('cart-items',list())
            
#             for i in range(len(cart_items)):
#                 if data.get("PName") == cart_items[i]["PName"]:
#                     cart_items[i]["quantity"] = str(int(data.get("quantity", 0)) + int(cart_items[i]["quantity"]))
#                     break
#             else:  
#                 cart_items.append(data)

#             request.session['cart-items'] = cart_items
#             return JsonResponse({"status": "success", "data": data})
#         except json.JSONDecodeError as e:
#             return JsonResponse({"status": "error", "message": str(e)})
