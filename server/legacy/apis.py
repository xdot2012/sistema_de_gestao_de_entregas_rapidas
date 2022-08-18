import datetime
from decimal import Decimal

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from routing.router import get_route
from .serializers import ClientSerializer, DeliveryManSerializer, OrderSerializer
from .models import Client, DeliveryMan, Order, OrderProduct
from rest_framework.response import Response
from django.db import transaction
from routing.models import ClientAddress, Branch
from django.core.exceptions import ObjectDoesNotExist


class OrderApiView(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        if request.data['appointment']:
            today = datetime.datetime.now()
            appointment_time = datetime.datetime.strptime(request.data['appointment'], "%H:%M")
            request.data['appointment'] = today.replace(
                hour=appointment_time.hour,
                minute=appointment_time.minute,
                second=0)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            order_obj = Order.objects.create(client_id=request.data['client'],
                                             created_by=request.user,
                                             delivery_type=request.data['delivery_type'],
                                             payment_method=request.data['payment_method'],
                                             address_id=request.data['address'],
                                             is_paid=request.data['is_paid'],
                                             total_value=Decimal(request.data['total_pedido']),
                                             change=Decimal(request.data['valor_troco']),
                                             payment=Decimal(request.data['total_esperado']),
                                             appointment=request.data['appointment'])

            for item in request.data['products']:
                OrderProduct.objects.create(order_id=order_obj.pk, name=item['name'], quantity=item['quantity'])

        return Response(self.serializer_class(order_obj).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(finished_on=None, active=True, created_by=request.user)
        queryset = sorted(queryset, key=lambda i: i.started_on)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def history(self, request, *args, **kwargs):
        queryset = Order.objects.filter(active=True, created_by=request.user)
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

    def get(self, request, *args, **kwargs):
        queryset = self.queryset(created_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = Client.objects.filter(created_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def filter(self, request, *args, **kwargs):
        queryset = self.queryset(created_by=request.user, **request.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_address = request.data['address']

        with transaction.atomic():
            client = Client.objects.create(
                name=serializer.validated_data['name'],
                phone=serializer.validated_data['phone'],
                created_by=request.user
            )
            branch = Branch.objects.filter(active=True, created_by=request.user).first()
            route = get_route(branch.longitude, branch.latitude, client_address['longitude'], client_address['latitude'])
            if route:
                distance = route['distance']
            else:
                distance = 0
            ClientAddress.objects.create(**client_address, client=client, distance=distance)

        return Response(self.serializer_class(client).data, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True)
    def name_phone(self, request, *args, **kwargs):
        try:
            client = Client.objects.get(pk=kwargs['pk'], created_by=request.user)
        except ObjectDoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        client.name = request.data['name']
        client.phone = request.data['phone']
        client.save()

        serializer = self.serializer_class(client, many=False)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

