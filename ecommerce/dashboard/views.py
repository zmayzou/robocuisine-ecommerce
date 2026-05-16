from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Sum

from products.models import Product, Category
from orders.models import Order, OrderItem
from promotions.models import Giveaway

from .forms import ProductForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class DashboardHomeView(StaffRequiredMixin, View):

    def get(self, request):

        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.count()
        total_giveaways = Giveaway.objects.count()

        recent_orders = Order.objects.order_by('-created_at')[:5]

        total_revenue = Order.objects.filter(
            status='confirmed'
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        best_product = OrderItem.objects.values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by(
            '-total_quantity'
        ).first()

        context = {
            'total_products': total_products,
            'total_categories': total_categories,
            'total_orders': total_orders,
            'total_giveaways': total_giveaways,
            'recent_orders': recent_orders,
            'total_revenue': total_revenue,
            'best_product': best_product
        }

        return render(request, 'dashboard/home.html', context)


class DashboardProductListView(StaffRequiredMixin, View):

    def get(self, request):

        products = Product.objects.all().order_by('-created_at')

        context = {
            'products': products
        }

        return render(request, 'dashboard/products.html', context)


class DashboardProductCreateView(StaffRequiredMixin, View):

    def get(self, request):

        form = ProductForm()

        context = {
            'form': form
        }

        return render(request, 'dashboard/product_form.html', context)

    def post(self, request):

        reference = request.POST.get('reference')
        stock = int(request.POST.get('stock') or 0)

        existing_product = Product.objects.filter(
            reference=reference
        ).first()

        if existing_product:

            existing_product.stock += stock
            existing_product.is_available = True
            existing_product.save()

            messages.success(
                request,
                "Produit déjà existant : la quantité du stock a été augmentée."
            )

            return redirect('dashboard_products')

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Produit ajouté avec succès."
            )

            return redirect('dashboard_products')

        context = {
            'form': form
        }

        return render(request, 'dashboard/product_form.html', context)


class DashboardProductUpdateView(StaffRequiredMixin, View):

    def get(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        form = ProductForm(instance=product)

        context = {
            'form': form,
            'product': product
        }

        return render(request, 'dashboard/product_form.html', context)

    def post(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Produit modifié avec succès."
            )

            return redirect('dashboard_products')

        context = {
            'form': form,
            'product': product
        }

        return render(request, 'dashboard/product_form.html', context)


class DashboardProductDeleteView(StaffRequiredMixin, View):

    def get(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id
        )

        product.delete()

        messages.success(
            request,
            "Produit supprimé avec succès."
        )

        return redirect('dashboard_products')