from django.contrib import admin
from .models import Product, Cart, HelpRequest, ContactMessage, UserProfile, UserLogin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'top_selling', 'created_at')
    list_filter = ('category', 'top_selling')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size', 'quantity', 'status', 'email', 'phone', 'created_at')
    list_editable = ('status',) 
    ordering = ('-created_at',)
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'order_id','product__name', 'email', 'phone')

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    list_per_page = 25

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    list_per_page = 25

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_login', 'can_access_admin')
    list_editable = ('can_login', 'can_access_admin')

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address')
    list_filter = ('login_time',)

