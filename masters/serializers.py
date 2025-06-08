from rest_framework import serializers

from .models import Master


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ["id", "name", "surname", "patronymic", "description", "specialty"]
