from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    number = PhoneNumberField(region="RU", verbose_name="Телефон", unique=False)
    tg_id = models.IntegerField(blank=True, null=True, verbose_name="Telegram ID")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        db_table = "clients"

    def __str__(self) -> str:
        return str(self.number)

    @property
    def appointments(self):
        return self.appointment_set.all()
