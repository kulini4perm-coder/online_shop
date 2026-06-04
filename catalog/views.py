from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .services import ProductService
from .models import Category

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductService.get_all_published_products()

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

class CategoryProductListView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category_id = self.kwargs.get('pk')
        return ProductService.get_products_by_category(self.category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.category_id)
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")

        return render(request, self.template_name, {'feedback': f'Спасибо, {name}! Сообщение получено.'})

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Создание товара
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Приравниваем поле owner к текущему авторизованному пользователю
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Редактирование товара
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        # Проверяем, является ли текущий пользователь владельцем
        if product.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта!")
        return product

# Удаление товара
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        # Условия доступа
        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator or self.request.user.is_superuser):
            raise PermissionDenied("У вас нет прав для удаления этого продукта!")

        return product


# Контроллер для отмены публикации
class SwitchPublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Меняем статус публикации на противоположный
        product.is_published = not product.is_published
        product.save()

        return redirect('catalog:product_detail', pk=product.pk)
