from django.db import models


class Specialty(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "specialty"
        verbose_name_plural = "specialties"
        db_table = "specialty"

    def __str__(self) -> str:
        return str(self.name)
