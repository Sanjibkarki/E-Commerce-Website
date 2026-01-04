from django.contrib import admin
from Home.models import Product

admin.site.site_header = "E-Commerce Recommendation Admin"
admin.site.site_title = "E-Commerce Recommendation Admin Portal"

admin.site.register(Product)
