from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserChangePasswordForm
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from config.settings import EMAIL_HOST_USER
import secrets


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Пожалуйста, пройдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def change_password(
        request,
):
    if request.method == "POST":
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(
                    email=form.cleaned_data.get("email"), is_active=True
                )
                print(user)
            except ObjectDoesNotExist:
                return render(
                    request,
                    "users/change_password.html",
                    {"form": UserChangePasswordForm()},
                )
            finally:
                new_password = User.make_random_password(12)
                user.set_password(new_password)
                user.save()
                print(f"Письмо отправлено{user.email}")
                send_mail(
                    subject="Новый пароль",
                    message=f"Ваш новый пароль: {new_password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return redirect(reverse("users:login"))
    elif request.method == "GET":
        return render(
            request,
            "users/change_password.html",
            {"form": UserChangePasswordForm()},
        )
