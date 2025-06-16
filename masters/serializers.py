from rest_framework import serializers

from specialties.models import Specialty

from .models import Master


class MasterSerializer(serializers.ModelSerializer):
    specialty = serializers.CharField(source='specialty.name')
    
    class Meta:
        model = Master
        fields = ["id", "name", "surname", "patronymic", "description", "specialty"]
