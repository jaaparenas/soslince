import json
from django.db.models import Q
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from core.filters import CustomSearchFilter
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAdminUser
from django.contrib.auth import get_user_model

from core.models import Staff
from core.serializers.staff import StaffSerializer, StaffListSerializer

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class StaffViewSet (viewsets.ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, CustomSearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return get_user_model().objects.filter(Q(is_superuser=True) | Q(is_staff=True)).all()
        elif user.is_staff:
            return get_user_model().objects.filter(Q(is_superuser=True) | Q(is_staff=True)).filter(id=user.id).all()
        return get_user_model().objects.none()

    @action(detail=False, methods=['get'], url_path='lts')
    def lts(self, request):
        queryset = self.get_queryset().select_related('staff').all()
        serializer = StaffListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='password')
    def password(self, request, *args, **kwargs):
        password = request.data.get('password')
        user = get_user_model().objects.filter(id=kwargs['pk']).first()
        user.set_password(password)
        user.save()
        return Response({})
