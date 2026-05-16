from django.contrib import admin

from .models import (
    Category,
    Product,
    Review
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'created_at'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'price',
        'stock',
        'is_available',
        'created_at'
    ]

    list_filter = [
        'is_available',
        'created_at'
    ]

    search_fields = [
        'name',
        'reference'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'product',
        'user',
        'rating',
        'created_at'
    ]

    list_filter = [
        'rating',
        'created_at'
    ]

    search_fields = [
        'product__name',
        'user__username'
    ]