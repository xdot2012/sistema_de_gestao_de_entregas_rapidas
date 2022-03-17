from django.urls import path, include
from rest_framework import routers
from legacy import views
from .apis import BranchApiView, ClientViewSet, GenerateRouteAPI, DeliveryManViewSet, OrderApiView

# Api routes
router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'deliveryman', DeliveryManViewSet)
router.register(r'orders', OrderApiView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/routes/generate/', GenerateRouteAPI.as_view()),
    path('api/branches/', BranchApiView.as_view()),
    path('', views.HomeView.as_view(), name='home'),
]
