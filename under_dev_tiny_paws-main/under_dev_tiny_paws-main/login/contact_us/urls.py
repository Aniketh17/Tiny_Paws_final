from django.urls import path, include
from contact_us.views import contact_view
urlpatterns = [
    path('contact/', contact_view, name='contact_view'),
    # path('success/', contact_success, name='contact_success'),


]