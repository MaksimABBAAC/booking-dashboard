from django.db import models
from django.urls import reverse

# Create your models here.
class Masters(models.Model):

    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150)
    description = models.TextField()


    class Meta:
        verbose_name = "master"
        verbose_name_plural = "masters"
        db_table = 'masters'


    