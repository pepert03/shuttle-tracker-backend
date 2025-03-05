from django.urls import path
from .views import get_driver_location

urlpatterns = [
    path("location/", get_driver_location),
]
