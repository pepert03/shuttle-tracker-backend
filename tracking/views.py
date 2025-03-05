from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DriverLocation


@api_view(["GET"])
def get_driver_location(request):
    location = DriverLocation.objects.last()
    if location:
        return Response(
            {"latitude": location.latitude, "longitude": location.longitude}
        )
    return Response({"error": "No location found"}, status=404)
