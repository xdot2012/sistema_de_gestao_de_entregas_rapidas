from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import City


class LocationSerializer(Serializer):
    address = serializers.CharField(max_length=200)
    altitude = serializers.FloatField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class CitySerializer(ModelSerializer):
    
    class Meta:
        model = City
        fields = ['pk', 'name']