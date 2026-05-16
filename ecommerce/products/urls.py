from django.urls import path
from .views import ProductListView, ProductDetailView,AddReviewView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/review/',AddReviewView.as_view(),name='add_review'),
]