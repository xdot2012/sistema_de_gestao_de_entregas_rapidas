from django.urls import path, include
from .apis import ClientAddressViewSet, BranchApiView, LocationAPIView
from rest_framework import routers

# Api routes
router = routers.DefaultRouter()
router.register(r'address', ClientAddressViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/branches/', BranchApiView.as_view()),
    path('api/location/', LocationAPIView.as_view()),
]
