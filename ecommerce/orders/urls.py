from django.urls import path

from .views import CheckoutView, OrderListView, OrderSuccessView, OrderDetailView


urlpatterns = [
    path('',OrderListView.as_view(),name='order_detail'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('success/',OrderSuccessView.as_view(),name='order_success'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]