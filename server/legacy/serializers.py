from rest_framework import serializers
from .models import Local, Client, DeliveryMan


class DeliveryManSerializer(serializers.ModelSerializer):
    phone_format = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryMan
        fields = ['pk', 'name', 'status', 'vehicle_type', 'phone', 'phone_format', 'capacity']

    def get_phone_format(self, obj):
        return f'({obj.phone[0:2]}){obj.phone[2:7]}-{obj.phone[7:]}'


class ClientSerializer(serializers.ModelSerializer):
    phone_format = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['pk', 'name', 'phone', 'phone_format', 'number', 'street', 'district', 'code', 'reference', 'country_name', 'state_name', 'city_name']

    def get_phone_format(self, obj):
        return f'({obj.phone[0:2]}){obj.phone[2:7]}-{obj.phone[7:]}'


class LocalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Local
        fields = ['pk', 'name', 'latitude', 'longitude', 'user_id']

