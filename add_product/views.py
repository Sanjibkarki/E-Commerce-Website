from django.shortcuts import render,redirect,HttpResponse
from Posti.form import UploadForm
from Home.models import Upperwear,Lowerwear,Footwear
from .admin_required import admin_required
from itertools import chain
from django.http import JsonResponse
@admin_required
def form(request):
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            if category == "U":
                upper = Upperwear(product_name = form.cleaned_data.get('PName'),price= form.cleaned_data.get('PPrice'),quatity = form.cleaned_data.get('Quantity'),image = form.cleaned_data.get('Image'))
                upper.save()
            elif category == "L":
                lower = Lowerwear(product_name = form.cleaned_data.get('PName'),price= form.cleaned_data.get('PPrice'),quatity = form.cleaned_data.get('Quantity'),image = form.cleaned_data.get('Image'))
                lower.save()
            else:
                foot = Footwear(product_name = form.cleaned_data.get('PName'),price= form.cleaned_data.get('PPrice'),quatity = form.cleaned_data.get('Quantity'),image = form.cleaned_data.get('Image'))
                foot.save()
            return redirect('/')
    
    
    else:
        form = UploadForm()
        return render(request,'front_pages/add.html',{'form':form})

def viewOrders(request):
    return render(request,"front_pages/order.html")

def manageProduct(request):
    
    if request.method == "DELETE":
        name = request.GET.get('id')
        try:
            product = Upperwear.objects.filter(product_name=name).delete()
        except Upperwear.DoesNotExist:
            try:
                product = Lowerwear.objects.filter(product_name=name).delete()
            except Lowerwear.DoesNotExist:
                try:
                    product = Footwear.objects.filter(product_name=name).delete()
                except Footwear.DoesNotExist:
                    product = None 
        return JsonResponse({'detail':"product is deleted"})
    results = list(chain(
                Upperwear.objects.all(),
                Lowerwear.objects.all(),
                Footwear.objects.all()
            ))  
    
    return render(request,'front_pages/manage.html',{'all':results})