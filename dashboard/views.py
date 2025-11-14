
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Cart

from store.forms import ProductForm  


def can_access_dashboard(user):
    """
    Returns True if the user can access the dashboard:
    - Staff or superuser
    - OR userprofile.can_access_admin is True
    """
    return user.is_staff or user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.can_access_admin)

def staff_check(user):
    """Check if user is staff or superuser"""
    return user.is_staff or user.is_superuser


@login_required
def dashboard_home(request):
    if not can_access_dashboard(request.user):
        return redirect('home') 

    latest_products = Product.objects.all().order_by('-created_at')[:5]
    latest_orders = Cart.objects.all().order_by('-created_at')[:5]

    context = {
        'product_count': Product.objects.count(),
        'user_count': User.objects.count(),
        'order_count': Cart.objects.count(),
        'latest_products': latest_products,
        'latest_orders': latest_orders,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def products_list(request):
    if not can_access_dashboard(request.user):
        return redirect('home')
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products.html', {'products': products})

@login_required
def orders_list(request):
    if not can_access_dashboard(request.user):
        return redirect('home')
    orders = Cart.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})

@login_required
def users_list(request):
   
    if not staff_check(request.user):
        return redirect('home')

    users = User.objects.select_related('userprofile').all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'dashboard/users.html', context)


@login_required
def edit_product(request, product_id):
    if not staff_check(request.user):
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.sizes = request.POST.get('sizes')
        product.top_selling = bool(request.POST.get('top_selling'))
        product.trending = bool(request.POST.get('trending'))
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('products_list')

    return render(request, 'dashboard/edit_product.html', {'product': product})

@login_required
def edit_order(request, order_id):
    if not staff_check(request.user):
        return redirect('home')

    order = get_object_or_404(Cart, id=order_id)

    if request.method == "POST":
        order.status = request.POST.get('status')
        order.save()
        messages.success(request, "Order status updated!")
        return redirect('orders_list')

    return render(request, 'dashboard/edit_order.html', {'order': order})


@user_passes_test(staff_check)
def toggle_login(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = getattr(user, 'userprofile', None)

    if profile:
        profile.can_login = not profile.can_login
        profile.save()
        if profile.can_login:
            messages.success(request, f"{user.username} is now allowed to login.")
        else:
            messages.warning(request, f"{user.username} is now blocked from login.")
    else:
        messages.error(request, "User profile not found.")
    return redirect('users_list')

@user_passes_test(staff_check)
def toggle_admin_access(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = getattr(user, 'userprofile', None)

    if profile:
        profile.can_access_admin = not profile.can_access_admin
        profile.save()
        if profile.can_access_admin:
            messages.success(request, f"{user.username} now has dashboard/admin access.")
        else:
            messages.warning(request, f"{user.username}'s dashboard/admin access has been revoked.")
    else:
        messages.error(request, "User profile not found.")
    return redirect('users_list')



@user_passes_test(staff_check)
def toggle_admin_access(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = getattr(user, 'userprofile', None)
    if profile:
        profile.can_access_admin = not profile.can_access_admin
        profile.save()
        if profile.can_access_admin:
            messages.success(request, f"{user.username} can now access the dashboard.")
        else:
            messages.warning(request, f"{user.username} cannot access the dashboard anymore.")
    else:
        messages.error(request, "User profile not found.")
    return redirect('users_list')

from django.shortcuts import render, redirect
from store.forms import ProductForm

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    return render(request, 'dashboard/add_product.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from store.forms import ProductForm

def edit_product(request, id): 
    product = get_object_or_404(Product, id=id)
    form = ProductForm(instance=product)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    
    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})
from django.shortcuts import render, redirect
from store.forms import OrderForm
from django.contrib.auth.decorators import login_required

@login_required
def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list') 
    else:
        form = OrderForm()
    return render(request, 'dashboard/add_order.html', {'form': form})
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm 

@login_required
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return redirect('users_list')  
    else:
        form = UserForm()
    return render(request, 'dashboard/add_user.html', {'form': form})
