from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ContactsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView, SwitchPublishView, CategoryListView, CategoryProductListView
)

app_name = 'catalog'

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    # Настраиваем кеширование для страницы информации о продукте:
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/switch-publish/', SwitchPublishView.as_view(), name='switch_publish'),
    path('category/<int:pk>/', CategoryProductListView.as_view(), name='category_products'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),

]

