from django.urls import path, include
from rest_framework import routers
from legacy import views
from .apis import ClientViewSet, DeliveryManViewSet, OrderApiView

# Api routes
router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'deliveryman', DeliveryManViewSet)
router.register(r'orders', OrderApiView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('home/', views.HomeView.as_view(), name='home'),
    path('', views.vue_serve, name='vue'),
]
