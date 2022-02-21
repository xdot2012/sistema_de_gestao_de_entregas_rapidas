from rest_framework import serializers
from .models import Local, Client, DeliveryMan
from accounts.models import User


class DeliveryManSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMan
        fields = ['name', 'status', 'vehicle_type', 'phone', 'capacity'
                  ]
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'phone', 'number', 'street', 'district', 'code', 'reference', 'country_name', 'state_name', 'city_name']

class LocalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Local
        fields = ['pk', 'name', 'latitude', 'longitude', 'user_id']
