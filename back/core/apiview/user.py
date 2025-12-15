from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from core.models import Staff

class UserAPIView(APIView):
    permission_classes = ()

    def get(self, request):

        user = request.user
        if user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        if not user.is_staff:
            return Response({"message": "Staff not found"}, status=404)

        staff = Staff.objects.filter(user=user).first()
        if not staff:
            return Response({"message": "Staff not found"}, status=404)

        data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": 1 if user.is_superuser else (2 if user.is_staff else 3),
            "image": staff.image if staff else "",
            "phone": staff.phone if staff else "",
        }

        return Response(data)
