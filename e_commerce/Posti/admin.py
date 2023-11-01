from django.contrib import admin
from Posti.models import Customer,Ordermodel

class OrdermodelInline(admin.TabularInline):
    model = Ordermodel
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [('Customer Info', {'fields': ['customer']}), ]
    inlines = [OrdermodelInline]

admin.site.register(Customer, ProductAdmin)