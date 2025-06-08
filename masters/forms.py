from django import forms

from masters.models import Master
from specialties.models import Specialty


class MasterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["specialty"].queryset = Specialty.objects.all()
        self.fields["specialty"].empty_label = "Выберите специализацию"
        self.fields["specialty"].label = "Специализация"

    class Meta:
        model = Master
        fields = ["name", "surname", "patronymic", "description", "specialty"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "surname": forms.TextInput(attrs={"class": "form-input"}),
            "patronymic": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 60, "rows": 10}),
            "specialty": forms.Select(attrs={"class": "form-select"}),
        }
