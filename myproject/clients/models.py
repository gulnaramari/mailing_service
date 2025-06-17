from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="почта")
    surname = models.CharField(max_length=35, verbose_name="фамилия клиента")
    name = models.CharField(max_length=35, verbose_name="имя клиента")
    second_name = models.CharField(
        max_length=35, verbose_name="отчество клиента", blank=True, null=True
    )
    comment = models.TextField(verbose_name="комментарий", blank=True, null=True)

    @property
    def get_fullname(self):
        return f"{self.surname} {self.name}"

    def __str__(self):
        return self.get_fullname

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        permissions = [
            ("can_view_client", "Может просматривать клиентов"),
        ]
