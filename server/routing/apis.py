from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .router import get_location
from .serializers import LocationSerializer


class LocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer

    def post(self, request):
        address = request.data['address']
        location = get_location(address)
        serializer = self.serializer_class(location)

        return Response(serializer.data, status=status.HTTP_200_OK)


