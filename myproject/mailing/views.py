from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .forms import ScheduledMailingForm, ImmediateMailingForm
from .models import Message, Mailing, MailingTrying


class MessageCreateView(CreateView):
    model = Message
    fields = (
        "topic",
        "content",
    )
    success_url = reverse_lazy("mailing:list_message")


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = (
        "topic",
        "content",
    )
    success_url = reverse_lazy("mailing:list_message")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:list_message")


class MailingCreateView(CreateView):
    model = Mailing
    form_class = ScheduledMailingForm
    template_name = "mailing/mailing_create_options.html"
    success_url = reverse_lazy("mailing:list_mailing")


class ScheduledMailingCreateView(CreateView):
    model = Mailing
    form_class = ScheduledMailingForm
    template_name = "mailing/scheduled_mailing_form.html"
    success_url = reverse_lazy("mailing:list_mailing")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        if not mailing.first_mailing:
            mailing.first_mailing = now()
        mailing.save()
        form.save_m2m()
        return super().form_valid(form)


class ImmediateMailingCreateView(CreateView):
    model = Mailing
    form_class = ImmediateMailingForm
    template_name = "mailing/immediate_mailing_form.html"
    success_url = reverse_lazy("mailing:list_mailing")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.is_immediate = True
        mailing.frequency = Mailing.Frequency.ONCE
        mailing.save()
        form.save_m2m()
        return super().form_valid(form)


# @method_decorator(cache_page(60 * 1), name="dispatch")
class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.object.id
        context["success_count"] = MailingTrying.get_success_count(mailing_id)
        context["failure_count"] = MailingTrying.get_failure_count(mailing_id)
        context["sent_messages_count"] = (
            context["success_count"] + context["failure_count"]
        )
        return context


# @method_decorator(cache_page(60 * 1), name="dispatch")
class MailingListView(ListView):
    model = Mailing


class ActiveMailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_active_list.html"

    def get_queryset(self):
        return Mailing.objects.filter(status="RN")


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ("next_mailing", "frequency", "status", "clients", "mail")
    success_url = reverse_lazy("mailing:list_mailing")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:list_mailing")


class MailingTryingListView(ListView):
    model = MailingTrying
    template_name = "mailing/mailing_trying_list.html"


class MailingTryingDetailView(DetailView):
    model = MailingTrying
    template_name = "mailing/mailing_trying_detail.html"
