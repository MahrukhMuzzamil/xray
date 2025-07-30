from rest_framework import serializers
from .models import XRayScan

class XRayScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRayScan
        fields = '__all__'
