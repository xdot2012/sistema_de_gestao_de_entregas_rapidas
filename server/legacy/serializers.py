from rest_framework import serializers
from .models import Branch, Client, DeliveryMan, Order, OrderProduct, ClientAddress


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


class ClientAddressSerializer(serializers.ModelSerializer):
    format = serializers.SerializerMethodField(read_only=True)
    nominatin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ClientAddress
        fields = ['pk', 'format', 'nominatin', 'country_name', 'state_name', 'city_name', 'number', 'street', 'district', 'code', 'reference', 'created_on', 'client', 'latitude', 'longitude', 'altitude']

    def get_format(self, obj):
        return f'Rua {obj.street} nº{obj.number}, Bairro {obj.district} - {obj.city_name}/{obj.state_name}.CEP: {obj.code}'

    def get_nominatin(self, obj):
        return f'Rua {obj.street}, {obj.city_name}, {obj.state_name}, {obj.code}'


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

