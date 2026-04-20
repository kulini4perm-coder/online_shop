from django.urls import path
from . import views
from .views import product_detail


app_name = 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
