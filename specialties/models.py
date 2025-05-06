from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "specialty"
        verbose_name_plural = "specialties"
        db_table = 'specialty'
    
    def __str__(self) -> str:
        return str(self.name)
    
    def delete(self, *args, **kwargs):
        if self.master_set.exists():  # Проверяем, есть ли мастера
            raise models.ProtectedError(
                "Невозможно удалить специальность, так как к ней привязаны мастера",
                self.master_set.all()
            )
        super().delete(*args, **kwargs)