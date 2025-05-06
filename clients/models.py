from django.db import models

class Client(models.Model):
    number = models.CharField(max_length=11, verbose_name="Номер телефона")
    tg_id = models.IntegerField(blank=True, null=True, verbose_name="Telegram ID")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        db_table = 'clients'
        ordering = ['number']

    def __str__(self) -> str:
        return self.number