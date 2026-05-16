from django.views import View
from django.shortcuts import render

from products.models import Product


class HomeView(View):

    def get(self, request):

        products = Product.objects.filter(is_available=True)

        context = {'products': products}

        return render(request,'core/home.html',context)