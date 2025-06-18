from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from .models import Client
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from myproject.mailing.models import Mailing


def base(request):
    unique = Client.objects.values("email").distinct().count()
    mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="RN").count()
    active_mailings_list = Mailing.objects.filter(status="RN")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"You have new message from {name}({email}): {message}")
    return render(
        request,
        "clients/base.html",
        {
            "unique_clients": unique,
            "total_mailings": mailings,
            "active_mailings": active_mailings,
            "active_mailings_list": active_mailings_list,
        },
    )


def home(request):
    unique = Client.objects.values("email").distinct().count()
    mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="RN").count()
    active_mailings_list = Mailing.objects.filter(status="RN")
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
    context = {
        "unique_clients": unique,
        "total_mailings": mailings,
        "active_mailings": active_mailings,
        "active_mailings_list": active_mailings_list,
    }

    return render(request, "clients/main.html", context)


class ClientCreateView(CreateView):
    model = Client
    fields = (
        "email",
        "name",
        "surname",
        "second_name",
        "comment",
    )
    success_url = reverse_lazy("clients:list_client")


class ClientDetailView(DetailView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = (
        "email",
        "name",
        "surname",
        "second_name",
        "comment",
    )
    success_url = reverse_lazy("clients:list_client")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("clients:list_client")
