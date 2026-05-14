from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hexmodal.models import Payload, Device, StatusChoices

from hexmodal.serializers import PayloadSerializer


class PayloadView(APIView):
    """
    Basic view to receive payloads - requires token authentication.

    Duplicate payloads are ignored. If the associated Device is not present, we will create it.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
