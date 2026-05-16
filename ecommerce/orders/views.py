from urllib import request
import uuid

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from cart.models import Cart
from .models import Order, OrderItem
from promotions.models import PromotionCode


class CheckoutView(LoginRequiredMixin, View):

    def get(self, request):

        cart = Cart.objects.get(user=request.user)

        context = {
            'cart': cart,
            'items': cart.items.all(),
            'total': cart.get_total(),
            'discount': 0,
            'final_total': cart.get_total()
        }

        return render(
            request,
            'orders/checkout.html',
            context
        )

    def post(self, request):

        cart = Cart.objects.get(user=request.user)

        if not cart.items.exists():
            messages.error(request,"Votre panier est vide.")
            return redirect('cart_detail')
        
        total = cart.get_total()

        promo_code = request.POST.get('promo_code')

        if promo_code:

            try:
                promotion = PromotionCode.objects.get(
                    code=promo_code,
                    is_active=True
                )

                discount = (
                    total *
                    promotion.discount_percentage
                ) / 100

                total -= discount

                messages.success(
                    request,
                    f"Code promo appliqué : -{promotion.discount_percentage}%"
                )

            except PromotionCode.DoesNotExist:

                messages.error(
                    request,
                    "Code promotionnel invalide."
                )

        order = Order.objects.create(
            user=request.user,
            order_number=f"CMD-{uuid.uuid4().hex[:10].upper()}",
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_price=total,
            status='pending'
        )

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            product = item.product

            if product.stock >= item.quantity:

                product.stock -= item.quantity

                if product.stock == 0:
                    product.is_available = False

                product.save()

        cart.items.all().delete()

        return redirect(
            'order_success'
        )


class OrderSuccessView(LoginRequiredMixin, View):

    def get(self, request):

        return render(
            request,
            'orders/success.html'
        )


class OrderListView(LoginRequiredMixin, View):

    def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')

        context = {
            'orders': orders
        }

        return render(
            request,
            'orders/list.html',
            context
        )


class OrderDetailView(LoginRequiredMixin, View):

    def get(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        context = {
            'order': order,
            'items': order.items.all()
        }

        return render(
            request,
            'orders/detail.html',
            context
        )