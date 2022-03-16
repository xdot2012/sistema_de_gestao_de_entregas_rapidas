from rest_framework.serializers import Serializer
from rest_framework import serializers


class LocationSerializer(Serializer):
    address = serializers.CharField(max_length=200)
    altitude = serializers.FloatField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
