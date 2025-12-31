from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Customer, Staff
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        data = request.data
        login = data.get('login') or data.get('username') or data.get('phone') or data.get('email')
        password = data.get('password')

        if not login or not password:
            return Response({'detail': 'Provide login and password'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.filter(username=login).first()
        if not user:
            user = User.objects.filter(email=login).first()

        if not user:
            cust = Customer.objects.filter(phone=login).first()
            if cust:
                user = cust.user

        if not user:
            staff = Staff.objects.filter(phone=login).first()
            if staff:
                user = staff.user

        if not user or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
