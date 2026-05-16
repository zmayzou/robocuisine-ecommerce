from django.views import View

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from orders.models import Order
from promotions.models import Participant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib import messages


class RegisterView(View):

    def get(self, request):

        return render(
            request,
            'accounts/register.html'
        )

    def post(self, request):

        username = request.POST.get('username')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:

            messages.error(
                request,
                "Les mots de passe ne correspondent pas."
            )

            return redirect('register')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Ce nom d'utilisateur existe déjà."
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)

        messages.success(
            request,
            "Compte créé avec succès."
        )

        return redirect('home')


class LoginView(View):

    def get(self, request):

        return render(
            request,
            'accounts/login.html'
        )

    def post(self, request):

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(
                request,
                "Connexion réussie."
            )

            return redirect('home')

        messages.error(
            request,
            "Identifiants invalides."
        )

        return redirect('login')


class LogoutView(View):

    def get(self, request):

        logout(request)

        messages.success(
            request,
            "Déconnexion réussie."
        )

        return redirect('home')
    
class UserDashboardView(LoginRequiredMixin, View):

    def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        )

        total_orders = orders.count()

        total_spent = sum(
            order.total_price
            for order in orders
        )

        latest_order = orders.order_by(
            '-created_at'
        ).first()

        total_participations = Participant.objects.filter(
            user=request.user
        ).count()

        context = {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'latest_order': latest_order,
            'total_participations': total_participations
        }

        return render(
            request,
            'accounts/dashboard.html',
            context
        )