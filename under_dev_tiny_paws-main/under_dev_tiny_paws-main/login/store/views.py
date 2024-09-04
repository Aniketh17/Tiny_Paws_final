from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
   

def product_list(request):
    # Fetch categories with their related products
    categories = Category.objects.prefetch_related('products').all()

    # Initialize a dictionary to hold filtered and sorted products for each category
    filtered_categories = []

    # Apply search and sort filters
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')

    for category in categories:
        
        products = category.products.all()

       
        if query:
            products = products.filter(name__icontains=query)

        
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'name_asc':
            products = products.order_by('name')
        elif sort_by == 'name_desc':
            products = products.order_by('-name')

        filtered_categories.append({'category': category, 'products': products})

    return render(request, 'store/product_list.html', {'filtered_categories': filtered_categories})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user  # Use the request user directly

    # Create or update the CartItem instance using the User instance
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=user
    )

    if not created:
        # Increment quantity if the item already exists
        cart_item.quantity += 1
    cart_item.save()

    return redirect('store:cart_view')  # Use the app namespace 'store'

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@require_POST
@login_required
def update_cart(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
    
    cart_item.save()
    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    return JsonResponse({'success': True})


 

@login_required
def checkout(request):
    if request.method == 'POST':
        # Retrieve and delete the cart items for the user
        cart_items = CartItem.objects.filter(user=request.user)
        cart_items.delete()
        
        # Redirect to the checkout confirmation page
        return redirect('store:checkout_confirmation')

    # Retrieve the cart items and total for GET requests (viewing the checkout page)
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})
def checkout_confirmation(request):
    return render(request, 'store/checkout_confirmation.html')