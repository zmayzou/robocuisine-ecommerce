from django.urls import path

from .views import (
    DashboardHomeView,
    DashboardProductListView,
    DashboardProductCreateView,
    DashboardProductUpdateView,
    DashboardProductDeleteView
)


urlpatterns = [

    path(
        '',
        DashboardHomeView.as_view(),
        name='dashboard_home'
    ),

    path(
        'products/',
        DashboardProductListView.as_view(),
        name='dashboard_products'
    ),

    path(
        'products/add/',
        DashboardProductCreateView.as_view(),
        name='dashboard_product_add'
    ),

    path(
        'products/<int:product_id>/edit/',
        DashboardProductUpdateView.as_view(),
        name='dashboard_product_edit'
    ),

    path(
        'products/<int:product_id>/delete/',
        DashboardProductDeleteView.as_view(),
        name='dashboard_product_delete'
    ),

]