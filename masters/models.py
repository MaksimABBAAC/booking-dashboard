from django.db import models
from specialties.models import Specialty

class Master(models.Model):

    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150)
    description = models.TextField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "master"
        verbose_name_plural = "masters"
        db_table = 'masters'


