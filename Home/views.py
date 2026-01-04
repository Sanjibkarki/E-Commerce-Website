from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework.authtoken.models import Token
from .models import Product
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from API.models import Order
from .recommend import ContentRecommender
from .recommender import recommend_products
from .forms import ProductForm
from django.urls import reverse
 


@method_decorator(cache_control(no_store=True,no_cache=True), name='dispatch')
class Index(View):    
    def get(self,request):
        token = None 
        print(Product.objects.all().values())
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
        return render(request, "frontpage/main.html")
    


class CartView(View):
    def get(self, request):
        return render(request, 'frontpage/cart.html')
    


@method_decorator(staff_member_required, name='dispatch')
class AdminOrders(View):
    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        return render(request, 'frontpage/admin_orders.html', {'orders': orders})


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetail(View):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return render(request, 'frontpage/admin_order_detail.html', {'error': 'Order not found'})
        return render(request, 'frontpage/admin_order_detail.html', {'order': order})

    
def product_search(request):
    query = request.GET.get("query", "")

    recommendproduct = ContentRecommender()

    if query:
        # ContentRecommender expects an exact product Name; try it first
        recs_df = recommendproduct.recommend(query, top_n=3)

        if recs_df is not None and not recs_df.empty:
            recommended = recs_df.to_dict(orient="records")
        else:
            # fallback: treat query as a search term and use token-based recommender
            prods = recommend_products(query, top_n=3)
            # convert Product objects to dicts similar to the DataFrame output
            recommended = []
            for p in prods:
                try:
                    image = p.Image
                except Exception:
                    image = p.Image.name if getattr(p, 'Image', None) else ""
                recommended.append({
                    "uuid": str(p.uuid),
                    "Name": p.Name,
                    "Description": p.Description,
                    "Image": image,
                    "Price": float(p.Price),
                    "category": dict(Product._meta.get_field('category').choices).get(p.category, p.category)
                })
    else:
        recommended = []

    return render(
        request,
        "frontpage/product_search.html",
        {"query": query, "recommended": recommended}
    )


@method_decorator(staff_member_required, name='dispatch')
class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'frontpage/add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        return render(request, 'frontpage/add_product.html', {'form': form})

