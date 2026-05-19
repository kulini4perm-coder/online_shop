from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")

        return render(request, self.template_name, {'feedback': f'Спасибо, {name}! Сообщение получено.'})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

