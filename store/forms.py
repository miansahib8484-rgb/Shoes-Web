from django import forms
from .models import Cart, HelpRequest


class CartForm(forms.ModelForm):
  
    DEFAULT_SIZES = [
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    size = forms.ChoiceField(
        choices=DEFAULT_SIZES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )

    class Meta:
        model = Cart
        fields = ['email', 'phone', 'address', 'quantity', 'size']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3,
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
     
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product:
           
            if hasattr(product, 'sizes') and product.sizes:
                if isinstance(product.sizes, str):
                    size_list = [s.strip() for s in product.sizes.split(',')]
                    self.fields['size'].choices = [(s, s) for s in size_list]
                elif isinstance(product.sizes, (list, tuple)):
                    self.fields['size'].choices = [(s, s) for s in product.sizes]
            else:
             
                self.fields['size'].choices = self.DEFAULT_SIZES

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        return qty


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 4,
                'required': True
            }),
        }


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'top_selling', 'trending', 'image', 'description']  # added description
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
        }

from django import forms
from .models import Order  # make sure you have an Order model

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity', 'status']  # adjust fields according to your Order model
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'customer', 'quantity', 'status']
