
from django.urls import path
from .views import service_list, service_detail


urlpatterns = [
    path('', service_list, name='service-list'),
    path('<int:pk>/', service_detail, name='service-detail'),
]
