from django.contrib import admin
from wood_house.products.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "category", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["category", "created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    llist_display = ["name", "is_active", "created_at"]
    search_fields = ["name"]
    list_filter = ["is_active"]
