import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer, DeliveryManSerializer, OrderSerializer
from .models import Client, DeliveryMan, Order, OrderProduct
from rest_framework.response import Response
from django.db import transaction
from routing.models import ClientAddress
from django.core.exceptions import ObjectDoesNotExist


class OrderApiView(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            order_obj = Order.objects.create(client_id=request.data['client'],
                                             created_by=request.user,
                                             delivery_type=request.data['delivery_type'],
                                             address_id=request.data['address'],
                                             is_paid=request.data['is_paid'])

            for item in request.data['products']:
                OrderProduct.objects.create(order_id=order_obj.pk, name=item['name'], quantity=item['quantity'])

        return Response(self.serializer_class(order_obj).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(finished_on=None, active=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def history(self, request, *args, **kwargs):
        queryset = Order.objects.filter(active=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def cancel(self, request, *args, **kwargs):
        orders = list(map(int, request.data['orders']))
        queryset = Order.objects.filter(pk__in=orders)
        queryset.update(active=False, modified_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def deliver(self, request, *args, **kwargs):
        orders = list(map(int, request.data['orders']))
        queryset = Order.objects.filter(pk__in=orders)
        queryset.update(ready_on=datetime.datetime.now(), modified_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def finish(self, request, *args, **kwargs):
        orders = list(map(int, request.data['orders']))
        queryset = Order.objects.filter(pk__in=orders)
        queryset.update(finished_on=datetime.datetime.now(), is_paid=True, modified_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def reset(self, request, *args, **kwargs):
        orders = list(map(int, request.data['orders']))
        queryset = Order.objects.filter(pk__in=orders)
        queryset.update(ready_on=None, finished_on=None, modified_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryManViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMan.objects.all()
    serializer_class = DeliveryManSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @action(methods=['POST'], detail=False)
    def filter(self, request, *args, **kwargs):
        filters = request.data
        client_list = Client.objects.filter(**filters)
        serializer = self.get_serializer(client_list, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_address = request.data['address']

        with transaction.atomic():
            client = Client.objects.create(name=serializer.validated_data['name'], phone=serializer.validated_data['phone'])
            ClientAddress.objects.create(**client_address, client=client)

        return Response(self.serializer_class(client).data, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True)
    def name_phone(self, request, *args, **kwargs):
        try:
            client = Client.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        client.name = request.data['name']
        client.phone = request.data['phone']
        client.save()

        serializer = self.serializer_class(client, many=False)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

