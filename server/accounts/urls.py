from django.urls import path, include
from accounts.apis import UserViewSet, AuthToken
from rest_framework import routers

# Api routes
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('token/', AuthToken.as_view(), name='get-token'),
    path('', include(router.urls)),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

