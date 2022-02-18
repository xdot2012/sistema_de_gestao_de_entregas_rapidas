from rest_framework import serializers
from .models import Local, Client
from accounts.models import User


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'phone', 'number', 'street', 'district', 'code', 'reference', 'country_name', 'state_name', 'city_name']

class LocalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Local
        fields = ['pk', 'name', 'latitude', 'longitude', 'user_id']
