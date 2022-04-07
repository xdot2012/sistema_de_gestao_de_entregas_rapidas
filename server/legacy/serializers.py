from rest_framework import serializers
from .models import Client, DeliveryMan, Order, OrderProduct
from routing.serializers import ClientAddressSerializer


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['pk', 'name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    address = ClientAddressSerializer(read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    products = OrderProductSerializer(read_only=True, many=True)
    key = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['pk', 'address', 'client', 'delivery_type', 'created_on', 'modified_on', 'ready_on', 'finished_on', 'created_by',
                  'modified_by', 'products', 'is_paid', 'payment_method', 'client_name', 'key']

    def get_key(self, obj):
        return f'{obj.pk}{obj.modified_on}{obj.ready_on}'


class DeliveryManSerializer(serializers.ModelSerializer):
    phone_format = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryMan
        fields = ['pk', 'name', 'status', 'vehicle_type', 'phone', 'phone_format', 'capacity']

    def get_phone_format(self, obj):
        return f'({obj.phone[0:2]}){obj.phone[2:7]}-{obj.phone[7:]}'


class ClientSerializer(serializers.ModelSerializer):
    phone_format = serializers.SerializerMethodField(read_only=True)
    addresses = ClientAddressSerializer(read_only=True, many=True)
    main_address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = ['pk', 'name', 'phone', 'phone_format', 'main_address', 'addresses']

    def get_phone_format(self, obj):
        return f'({obj.phone[0:2]}){obj.phone[2:7]}-{obj.phone[7:]}'

    def get_main_address(self, obj):
        address = obj.addresses.filter(active=True).first()
        if address is not None:
            return ClientAddressSerializer(address).data
        return None
