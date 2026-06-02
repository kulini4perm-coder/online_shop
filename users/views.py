from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserCreateForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save() # автоматически вызывает set_password()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис!'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")

# Редактирование профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
        model = User
        form_class = UserProfileForm
        template_name = 'users/profile.html'
        success_url = reverse_lazy('catalog:home')

        def get_object(self, queryset=None):
            # Пользователь редактирует только свой профиль
            return self.request.user

