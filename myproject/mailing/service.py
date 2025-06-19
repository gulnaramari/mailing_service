from datetime import  timedelta
from django.conf import settings
from django.utils import timezone

from django.core.mail import send_mail
from .models import Mailing, MailingTrying


def check_and_send_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        status__in=[Mailing.Status.CREATED, Mailing.Status.RUNNING],
        next_mailing__lte=now,
    ).exclude(last_try__gt=now - timedelta(minutes=1))

    for mailing in mailings:
        mailing.status = Mailing.Status.RUNNING
        mailing.last_try = now
        mailing.save()

        try:
            clients = mailing.clients.all()
            for client in clients:
                send_mail(
                    mailing.message.topic,
                    mailing.message.content,
                    settings.EMAIL_HOST_USER,
                    [client.email],
                    fail_silently=False,
                )

            MailingTrying.objects.create(
                last_mailing=now,
                status_trying="SC",
                server_response="Успешно",
                mailing=mailing,
            )

            if mailing.frequency != Mailing.Frequency.ONCE:
                mailing.set_next_mailing_after_send()
                mailing.status = Mailing.Status.CREATED
            else:
                mailing.status = Mailing.Status.FINISHED

            mailing.save()

        except Exception as e:
            MailingTrying.objects.create(
                last_mailing=now,
                status_trying="FL",
                server_response=str(e),
                mailing=mailing,
            )
            mailing.status = Mailing.Status.FAILED
            mailing.save()

#
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_and_send_mailings, "interval", minutes=1)
#     scheduler.start()
