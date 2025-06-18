from datetime import timedelta
from django.utils import timezone
from django.db import models
from myproject.clients.models import Client


class Message(models.Model):
    topic = models.CharField(max_length=35, verbose_name="тема письма")
    content = models.TextField(verbose_name="содержание письма")

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        permissions = [
            ("can_view_mailing", "Просмотр рассылок"),
            ("can_delete_mailing", "Отключение рассылок"),
        ]


class Mailing(models.Model):
    class Status(models.TextChoices):
        CREATED = "CR", "Создана"
        RUNNING = "RN", "Запущена"
        FINISHED = "FS", "Завершена"
        FAILED = "FL", "Ошибка"

    class Frequency(models.TextChoices):
        ONCE = "ON", "Один раз"
        DAILY = "DY", "Раз в день"
        WEEKLY = "WE", "Раз в неделю"
        MONTHLY = "MN", "Раз в месяц"

    first_mailing = models.DateTimeField(
        verbose_name="первая рассылка", null=True, blank=True
    )
    frequency = models.CharField(
        max_length=2,
        choices=Frequency.choices,
        default=Frequency.DAILY,
        verbose_name="Периодичность",
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="Статус",
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="mailing", verbose_name="Письмо"
    )
    next_mailing = models.DateTimeField(
        null=True, blank=True, verbose_name="Следующая рассылка"
    )
    is_immediate = models.BooleanField(
        default=False, verbose_name="Немедленная отправка"
    )
    last_try = models.DateTimeField(
        null=True, blank=True, verbose_name="Последняя попытка"
    )

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [
            ("can_view_mailing", "Просмотр рассылок"),
            ("can_delete_mailing", "Отключение рассылок"),
        ]

    def save(self, *args, **kwargs):
        if self.is_immediate:
            self.next_mailing = timezone.now()
            self.first_mailing = timezone.now()
        elif not self.next_mailing and self.first_mailing:
            self.next_mailing = self.first_mailing
        super().save(*args, **kwargs)

    def set_next_mailing_after_send(self):
        if self.frequency == self.Frequency.DAILY:
            self.next_mailing += timedelta(days=1)
        elif self.frequency == self.Frequency.WEEKLY:
            self.next_mailing += timedelta(weeks=1)
        elif self.frequency == self.Frequency.MONTHLY:
            self.next_mailing += timedelta(weeks=4)
        elif self.frequency == self.Frequency.ONCE:
            self.status = self.Status.FINISHED


class MailingTrying(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SC", "Успешно"
        FAILED = "FL", "Неуспешно"

    last_mailing = models.DateTimeField(verbose_name="последняя рассылка")
    status_trying = models.CharField(
        max_length=30, choices=Status.choices, verbose_name="статус попытки"
    )
    server_response = models.CharField(max_length=1000)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    @classmethod
    def get_success_count(cls, mailing_id):
        return cls.objects.filter(
            mailing_id=mailing_id, status_trying=cls.Status.SUCCESS
        ).count()

    @classmethod
    def get_failure_count(cls, mailing_id):
        return cls.objects.filter(
            mailing_id=mailing_id, status_trying=cls.Status.FAILED
        ).count()

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
