from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
        adresses = ClientAddress.objects.filter(pk__in=request.data['addresses'])
        path = get_path(branch.longitude, branch.latitude, adresses.values('longitude', 'latitude'))
        print(path)