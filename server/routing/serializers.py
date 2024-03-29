from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import ClientAddress, Branch, get_complete, get_format, get_nominatin


class ClientAddressSerializer(serializers.ModelSerializer):
    format = serializers.SerializerMethodField(read_only=True)
    nominatin = serializers.SerializerMethodField(read_only=True)
    complete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ClientAddress
        fields = ['pk', 'distance', 'complete', 'format', 'nominatin', 'country_name', 'state_name', 'city_name', 'number', 'street', 'district', 'code', 'reference', 'created_on', 'client', 'latitude', 'longitude', 'altitude']

    def get_complete(self, obj):
        return get_complete(obj)

    def get_format(self, obj):
        return get_format(obj)

    def get_nominatin(self, obj):
        return get_nominatin(obj)


class BranchSerializer(serializers.ModelSerializer):
    format = serializers.SerializerMethodField(read_only=True)
    nominatin = serializers.SerializerMethodField(read_only=True)
    complete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Branch
        fields = ['pk', 'complete', 'format', 'nominatin', 'country_name', 'state_name', 'city_name', 'number', 'street', 'district', 'code', 'reference', 'latitude', 'longitude', 'altitude']

    def get_complete(self, obj):
        return get_complete(obj)

    def get_format(self, obj):
        return get_format(obj)

    def get_nominatin(self, obj):
        return get_nominatin(obj)


class LocationSerializer(Serializer):
    address = serializers.CharField(max_length=200)
    altitude = serializers.FloatField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()