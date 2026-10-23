from .views import ThrottledObtainAuthToken, api_home
from .views import ThrottledObtainAuthToken
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
urlpatterns = [
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(
        'api/token/',
        ThrottledObtainAuthToken.as_view(),
        name='api-token',
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path('api/customers/', include('customers.urls')),
    path('api/services/', include('services.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
]