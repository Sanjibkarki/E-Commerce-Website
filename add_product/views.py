from django.shortcuts import render,redirect,HttpResponse
from Posti.form import UploadForm
from Home.models import Upperwear,Lowerwear,Footwear
# Create your views here.
def form(request):
    if request.user.is_authenticated and request.user.is_staff: 
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
        
    else:
        return HttpResponse("<p>You are not the admin only admin is allowed to view this page</p>")