from django.urls import path, include
from .apis import LocationAPIView

urlpatterns = [
    path('api/routes/location/', LocationAPIView.as_view()),
]
