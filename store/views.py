from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .models import Product, HelpRequest, ContactMessage, Cart
from .forms import CartForm, HelpRequestForm, SignupForm

def home(request):
    trending_products = Product.objects.filter(trending=True)
    flash_sale_products = Product.objects.filter(category='FlashSale')
    flipflop_products = Product.objects.filter(category='FlipFlops')
    women_products = Product.objects.filter(category='Women')
    men_products = Product.objects.filter(category='Men')
    top_products = Product.objects.filter(top_selling=True)
    sizes = [6, 7, 8, 9, 10]  # optional, can remove if you want dynamic sizes

    return render(request, 'store/home.html', {
        'trending_products': trending_products,
        'flash_sale_products': flash_sale_products,
        'flipflop_products': flipflop_products,
        'women_products': women_products,
        'men_products': men_products,
        'top_products': top_products,
        'sizes': sizes,  # optional
        # ❌ Don't assign size_list here
    })




# Category Pages
def men(request):
    products = Product.objects.filter(category='Men')
    sizes = [6, 7, 8, 9, 10]
    return render(request, 'store/men.html', {'products': products, 'sizes': sizes, 'category': 'Men'})


def women(request):
    products = Product.objects.filter(category='Women')
    sizes = [6, 7, 8, 9, 10]
    return render(request, 'store/women.html', {'products': products, 'sizes': sizes, 'category': 'Women'})


def flash_sale(request):
    products = Product.objects.filter(category='FlashSale')
    sizes = [6, 7, 8, 9, 10]
    return render(request, 'store/flashsale.html', {'products': products, 'sizes': sizes, 'category': 'FlashSale'})


def flipflop(request):
    products = Product.objects.filter(category__iexact='FlipFlops')
    sizes = [6, 7, 8, 9, 10]
    return render(request, 'store/flipflops.html', {'products': products, 'sizes': sizes, 'category': "FlipFlops"})


def top_selling_products(request):
    # Use the correct field name 'top_selling'
    products = Product.objects.filter(top_selling=True)
    return render(request, 'store/all_products.html', {
        'heading': 'Top Selling Products',
        'products': products
    })

def trending_products_view(request):
    # Get all trending products
    products = Product.objects.filter(trending=True)
    return render(request, 'store/all_products.html', {
        'heading': 'Trending Products',
        'products': products
    })

# Search
def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'query': query, 'results': results})


def filter_by_size(request, size):
    products = Product.objects.filter(sizes__icontains=str(size))
    sizes = [6, 7, 8, 9, 10]
    category = None  # explicitly define category
    return render(request, 'store/size_filter.html', {
        'products': products,
        'size': size,
        'sizes': sizes,
        'category': category
    })



def filter_by_category_size(request, category, size):
    products = Product.objects.filter(category__iexact=category, sizes__icontains=str(size))
    sizes = [6, 7, 8, 9, 10]
    return render(request, 'store/size_filter.html', {'products': products, 'size': size, 'sizes': sizes, 'category': category.capitalize()})


# Product Detail (✅ cleaned — no cart add here)
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes = [6, 7, 8, 9, 10]
    form = CartForm(product=product)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'form': form,
        'sizes': sizes
    })
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = CartForm(request.POST, product=product)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product
            cart_item.user = request.user
            cart_item.save()  # ✅ this writes to DB
            messages.success(request, f"{product.name} added to cart successfully!")
            return render(request, "store/cart_success.html", {"product": product})
        else:
            print("Form errors:", form.errors)  # ✅ debug any issues
    else:
        form = CartForm(product=product)

    return render(request, "store/product_detail.html", {"product": product, "form": form})

# About & Contact
def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not name or not email or not message_text:
            messages.error(request, "All fields are required.")
        else:
            ContactMessage.objects.create(name=name, email=email, message=message_text)
            messages.success(request, "Your message has been sent successfully.")

    return render(request, 'store/contact.html')


# Help
def help_view(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your help request has been submitted.")
            return redirect('help')
    else:
        form = HelpRequestForm()

    return render(request, 'store/help.html', {'form': form})


# All Products
def all_products(request, category=None):
    products = Product.objects.filter(category__iexact=category) if category else Product.objects.all()
    heading = f"{category} Shoes" if category else "All Products"
    return render(request, 'store/all_products.html', {'products': products, 'heading': heading, 'category': category})
# store/views.py
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # creates the User

            # Create profile only if it doesn't exist
            UserProfile.objects.get_or_create(user=user)

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})



# store/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User



class CustomLoginView(LoginView):
    template_name = 'store/login.html'

    def form_valid(self, form):
        user = form.get_user()
        
        if hasattr(user, 'userprofile') and not user.userprofile.can_login:
            messages.error(self.request, "Your account has been blocked. Contact admin.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return '/' 
        


class CustomLogoutView(LogoutView):
    next_page = '/'  

@login_required
def track_orders(request):
    
    orders = Cart.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'store/track.html', context)



@login_required
def cart_view(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': user_cart_items})


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from store.models import Product, Cart  

def staff_check(user):
    return user.is_staff or user.is_superuser

@user_passes_test(staff_check)
def dashboard_home(request):
    product_count = Product.objects.count()
    user_count = User.objects.count()
    cart_items = Cart.objects.count() 

    context = {
        'product_count': product_count,
        'user_count': user_count,
        'cart_count': cart_items,
    }

    return render(request, 'dashboard/home.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def checkout(request):
    if request.method == 'POST':
      
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('home')  

      
        cart_items.update(status='Pending')

       
        return render(request, 'store/order_success.html', {
            'cart_items': cart_items,
            'message': 'Your order has been placed successfully!'
        })

    return redirect('home')

