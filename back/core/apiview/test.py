from rest_framework.views import APIView
from rest_framework.response import Response

class TestAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        return Response({ "msg": "Hello World!"})