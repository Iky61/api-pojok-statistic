from rest_framework import serializers
from .models import Turnover


class TurnoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turnover
        fields = ['file']
