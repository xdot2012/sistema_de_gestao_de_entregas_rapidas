from django.urls import path, include
from .apis import LocationAPIView
from rest_framework import routers

# Api routes
router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/routes/location/', LocationAPIView.as_view()),
]
