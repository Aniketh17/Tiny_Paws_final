from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout-confirmation/', views.checkout_confirmation, name='checkout_confirmation'),  
]
