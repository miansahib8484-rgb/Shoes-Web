
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.products_list, name='products_list'),
    path('orders/', views.orders_list, name='orders_list'),
    path('users/', views.users_list, name='users_list'),
    
   
    path('toggle-login/<int:user_id>/', views.toggle_login, name='toggle_login'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin_access, name='toggle_admin_access'),

   
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('products/add/', views.add_product, name='add_product'),  # <-- This is the link for your button
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/', views.products_list, name='products_list'),
    path('orders/add/', views.add_order, name='add_order'),
    path('users/add/', views.add_user, name='add_user'),


]