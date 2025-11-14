from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, signup_view
from django.urls import path, include

urlpatterns = [
  
    path('', views.home, name='home'),
    path('men/', views.men, name='men'),
    path('women/', views.women, name='women'),
    path('flashsale/', views.flash_sale, name='flashsale'),
    path('flipflops/', views.flipflop, name='flipflops'),
    path('top-selling/', views.top_selling_products, name='top_selling_products'),
    path('trending/', views.trending_products_view, name='trending_products'),
    
   
    path('search/', views.search, name='search'),
    path('filter/size/<int:size>/', views.filter_by_size, name='filter_by_size'),
    path('filter/<str:category>/<int:size>/', views.filter_by_category_size, name='filter_by_category_size'),

    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('all/', views.all_products, name='all_products'),
    path('all/category/<str:category>/', views.all_products, name='all_products_category'),

    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_view, name='help'),
    path('about/', views.about, name='about'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('track-orders/', views.track_orders, name='track_order'),
    path('dashboard/', include('dashboard.urls')),
    path('checkout/', views.checkout, name='checkout'),

]

