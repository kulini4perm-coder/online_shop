from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import BlogEntry
from django.urls import reverse, reverse_lazy


class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/home.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return BlogEntry.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class BlogCreateView(CreateView):
    model = BlogEntry
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:home')

class BlogUpdateView(UpdateView):
    model = BlogEntry
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        # Возвращаемся на страницу статьи после редактирования
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
