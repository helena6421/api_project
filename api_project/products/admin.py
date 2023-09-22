from django.contrib import admin

from .models import Product, ProductStudent


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStudent)
class ProductStudentAdmin(admin.ModelAdmin):
    pass
