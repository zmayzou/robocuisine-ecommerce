from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, View):

    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        context = {
            'cart': cart,
            'items': cart.items.all(),
            'total': cart.get_total()
        }

        return render(
            request,
            'cart/detail.html',
            context
        )

class AddToCartView(LoginRequiredMixin, View):

    def get(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        if product.stock <= 0:
            messages.error(
                request,
                "Ce produit est actuellement en rupture de stock."
            )
            return redirect(
                'product_detail',
                slug=product.slug
            )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:

            if cart_item.quantity >= product.stock:
                messages.warning(
                    request,
                    "La quantité demandée dépasse le stock disponible."
                )
                return redirect('cart_detail')

            cart_item.quantity += 1
            cart_item.save()

        messages.success(
            request,
            "Produit ajouté au panier avec succès."
        )

        return redirect('cart_detail')

class RemoveFromCartView(LoginRequiredMixin, View):

    def get(self, request, item_id):

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        cart_item.delete()

        return redirect('cart_detail')
    
class UpdateCartItemView(LoginRequiredMixin, View):

    def post(self, request, item_id):

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()

        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        return redirect('cart_detail')