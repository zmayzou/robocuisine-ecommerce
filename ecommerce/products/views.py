from itertools import product
from urllib import request
from django.views import View 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductDetailView(View):

    def get(self, request, slug):

        product = get_object_or_404(
        Product,
        slug=slug
        )

        related_products = Product.objects.filter(
            category=product.category
        ).exclude(
            id=product.id
        )[:4]

        context = {
            'product': product,
            'related_products': related_products
        }

        return render(
            request,
            'products/detail.html',
            context
        )
    
class ProductListView(View):

    def get(self, request):

        search = request.GET.get('search')
        category_id = request.GET.get('category')

        products = Product.objects.all()

        if search:
            products = products.filter(name__icontains=search)

        if category_id:
            products = products.filter(category_id=category_id)

        paginator = Paginator(products, 6)

        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        categories = Category.objects.all()

        context = {
            'products': products,
            'categories': categories,
            'selected_category': category_id,
            'search': search
        }

        return render(request, 'products/list.html', context)


class ProductDetailView(View):

    def get(self, request, slug):

        product = get_object_or_404(
            Product,
            slug=slug
        )

        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]

        context = {
            'product': product,
            'related_products': related_products
        }

        return render(request, 'products/detail.html', context)

    
class AddReviewView(LoginRequiredMixin, View):

    def post(self, request, slug):

        product = get_object_or_404(
            Product,
            slug=slug,
            is_available=True
        )

        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

        messages.success(
            request,
            "Votre avis a été ajouté avec succès."
        )

        return redirect(
            'product_detail',
            slug=product.slug
        )