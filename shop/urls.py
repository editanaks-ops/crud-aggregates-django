from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # Товары
    path('', views.product_list, name='product_list'),
    path('product/new/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # Категории
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.create_category, name='create_category'),
    path('categories/<int:pk>/edit/', views.update_category, name='update_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # Аналитика
    path('analytics/', views.analytics_view, name='analytics'),
]