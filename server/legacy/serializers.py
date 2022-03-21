from rest_framework import serializers
from .models import Branch, Client, DeliveryMan, Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['pk', 'name', 'quantity']


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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['pk', 'name', 'latitude', 'longitude', 'state', 'country']


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    products = OrderProductSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['pk', 'client', 'delivery_type', 'created_on', 'modified_on', 'ready_on', 'finished_on', 'created_by',
                  'modified_by', 'products', 'is_paid', 'payment_method', 'client_name']

