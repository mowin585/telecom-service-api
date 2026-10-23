from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import ScopedRateThrottle


class ThrottledObtainAuthToken(ObtainAuthToken):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'
   


def api_home(request):
    return JsonResponse({
        "message": "Welcome to Telecom Service API",
        "endpoints": {
            "documentation": "/api/docs/",
            "schema": "/api/schema/",
            "customers": "/api/customers/",
            "services": "/api/services/",
            "subscriptions": "/api/subscriptions/",
            "authentication": "/api/token/"
        }
    })