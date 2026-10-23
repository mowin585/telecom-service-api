
from django.urls import path
from .views import subscription_list, subscription_detail


urlpatterns = [
    path('', subscription_list, name='subscription-list'),
    path('<int:pk>/', subscription_detail, name='subscription-detail'),
]
