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
    queryset = Branch.objects.all
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


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
        branch = Branch.objects.filter(active=True).first()
        orders_pk = list(map(int, request.data['orders']))
        orders_pk.sort()
        orders = Order.objects.filter(pk__in=orders_pk).order_by('address__id')
        points_to_visit = [
            {'longitude': branch.longitude,
             'latitude': branch.latitude,
             'order': None
             }
        ]
        for order in orders:
            points_to_visit.append({
                'longitude': order.address.longitude,
                'latitude': order.address.latitude,
                'order': order,
            })

        path = get_path(points_to_visit)
        data = []

        for i in range(0, len(points_to_visit)):
            data.append({
                'index': path['waypoints'][i]['waypoint_index'],
                'distance': path['waypoints'][i]['distance'],
                'name': path['waypoints'][i]['name'],
                'longitude': path['waypoints'][i]['location'][0],
                'latitude': path['waypoints'][i]['location'][1],
                'order': OrderSerializer(points_to_visit[path['waypoints'][i]['waypoint_index']]['order']).data,
                'point': [path['waypoints'][i]['location'][1], path['waypoints'][i]['location'][0]]
            })

        data = sorted(data, key=lambda k: k['index'])
        response = {
            'data': data,
            'route': path['route']
        }
        return Response(response, status=status.HTTP_200_OK)