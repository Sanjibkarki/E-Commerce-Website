from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from accounts.models import User

from .models import Upperwear,Lowerwear,Footwear
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework.authtoken.models import Token

@method_decorator(cache_control(no_store=True,no_cache=True), name='dispatch')
class Index(View):    
    def get(self,request):
        token = None 

        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)

        upperwear = Upperwear.objects.values().all()
        lowerwear = Lowerwear.objects.values().all()
        footwear = Footwear.objects.values().all()

        context = {
            'product': upperwear,
            'product2': lowerwear,
            'product3': footwear,
            'token': token,
        }

        return render(request, "index.html", context)
    

    