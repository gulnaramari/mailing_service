from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from myproject.mailing.models import Mailing, MailingTrying
from django.utils import timezone


class Command(BaseCommand):
    help = "Отправить последнюю созданную рассылку один раз без изменения статуса и периодичности"

    def handle(self, *args, **kwargs):
        mailing = Mailing.objects.filter(status=Mailing.Status.CREATED).last()

        if mailing:
            clients = mailing.clients.all()
            mail_subject = mailing.message.topic
            mail_content = mailing.message.content

            for client in clients:
                send_mail(
                    mail_subject,
                    mail_content,
                    settings.EMAIL_HOST_USER,
                    [client.email],
                    fail_silently=False,
                )

            MailingTrying.objects.create(
                last_mailing=timezone.now(),
                status_trying=True,
                server_response="Письма отправлены",
                mailing=mailing,
            )

            print(f'Рассылка "{mailing}" была успешно отправлена.')
        else:
            print("Нет созданных рассылок для отправки.")
