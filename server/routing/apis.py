from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from legacy.models import Order
from legacy.serializers import OrderSerializer
from .models import Branch, ClientAddress
from .router import get_location, get_path
from .serializers import BranchSerializer, ClientAddressSerializer, LocationSerializer
from rest_framework import viewsets, status


class BranchApiView(APIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Branch.objects.filter(created_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request, *args, **kwargs):
        queryset = self.queryset(client__created_by=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class LocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def post(self, request):
        address = request.data['address']
        location = get_location(address)
        serializer = self.serializer_class(location)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PathFinderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        branch = Branch.objects.filter(active=True, created_by=request.user).first()
        branch_index = f'{branch.longitude},{branch.latitude}'
        orders_pk = list(map(int, request.data['orders']))
        orders_pk.sort()
        orders = Order.objects.filter(pk__in=orders_pk).order_by('address__id')

        waypoints = {}
        waypoints[branch_index] = {
            'latitude': branch.latitude,
            'longitude': branch.longitude,
            'orders': [],
            'address': {
                'city_name': branch.city_name,
                'street': branch.street,
                'district': branch.district,
            }

        }

        for order in orders:
            order_index = f'{order.address.longitude},{order.address.latitude}'
            if order_index not in waypoints:
                waypoints[order_index] = {
                    'latitude': order.address.latitude,
                    'longitude': order.address.longitude,
                    'orders': [order],
                    'address': {
                        'city_name': order.address.city_name,
                        'street': order.address.street,
                        'district': order.address.district,
                    }
                }
            else:
                waypoints[order_index]['orders'].append(order)

        data = []
        if len(waypoints) > 1:
            path = get_path(waypoints)
            waypoint_array = list(waypoints.values())
            i = 0

            for item in path['waypoints']:
                w_id = item['waypoint_index']
                data.append({
                    'index': w_id,
                    'distance': item['distance'],
                    'name': waypoint_array[i]['address']['street'],
                    'longitude': waypoint_array[i]['longitude'],
                    'latitude': waypoint_array[i]['latitude'],
                    'orders': OrderSerializer(waypoint_array[i]['orders'], many=True).data,
                    'point': [waypoint_array[i]['latitude'], waypoint_array[i]['longitude']]
                })
                i += 1

            data = sorted(data, key=lambda i: i['index'])

            response = {
                'data': data,
                'route': path['route']
            }

        else:
            data.append({
                'index': 0,
                'distance': 0,
                'name': 'Sede',
                'longitude': branch.longitude,
                'latitude': branch.latitude,
                'orders': OrderSerializer(orders, many=True).data,
                'point': [branch.latitude, branch.longitude]
            })
            response = {
                'data': data,
                'route': {
                    'full_path': [[branch.latitude, branch.longitude]],
                    'legs': {
                        'steps': [],
                        'polyline': [],
                        'key': 0,
                    },
                    'duration': 0,
                    'distance': 0,
                }
            }

        return Response(response, status=status.HTTP_200_OK)