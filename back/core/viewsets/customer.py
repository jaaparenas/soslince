from datetime import datetime
from django.utils import timezone
from datetime import datetime, timezone as py_timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from core.models import Customer, CustomerLocation, CustomerSOS
from core.serializers.customer import CustomerSerializer
from core.serializers.customerLocation import CustomerLocationSerializer
from core.serializers.customerSOS import CustomerSosSerializer, CustomerSosPendingSerializer

from soslince.excel_serializer import ExcelSerializer
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class CustomerViewSet (viewsets.ModelViewSet):

    permission_classes = [IsStaffUser]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_staff=False).all()

    def get_permissions(self):
        #if self.action == 'create':
        #    return [IsSuperUser()]
        #else:
        return [IsStaffUser()]

    def list(self, request, *args, **kwargs):
        listReturn = super().list(request, *args, **kwargs)
        return listReturn

    @action(detail=False, methods=['post'], url_path='password')
    def password(self, request, *args, **kwargs):
        id = request.data.get('id')
        password = request.data.get('password')
        user = get_user_model().objects.filter(is_staff=False).filter(id=id).first()
        user.set_password(password)
        user.save()
        return Response({})

    @action(detail=False, methods=['get'], url_path='list_location')
    def list_locations(self, request, *args, **kwargs):
        user_id = request.query_params.get("userId")
        filter_param = request.query_params.get("filter")
        format = request.query_params.get("f")

        locations = CustomerLocation.objects.filter(
            customer=Customer.objects.filter(user=user_id).first()
        ).order_by('-id')

        if filter_param:
            start_date_str, end_date_str = filter_param.split(',')
            try:
                start_date = datetime.fromisoformat(start_date_str)
                end_date = datetime.fromisoformat(end_date_str)
                locations = locations.filter(timestamp__range=(start_date, end_date))
            except ValueError:
                pass

        if format == 'export':
            return ExcelDownload('location', locations)

        page = self.paginate_queryset(locations)
        if page is not None:
            serializer = CustomerLocationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerLocationSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list_sos')
    def list_sos(self, request, *args, **kwargs):
        user_id = request.query_params.get("userId")
        filter_param = request.query_params.get("filter")
        format = request.query_params.get("f")

        locations = CustomerSOS.objects.filter(
            customer=Customer.objects.filter(user=user_id).first()
        ).order_by('-id')

        if filter_param:
            start_date_str, end_date_str = filter_param.split(',')
            try:
                start_date = datetime.fromisoformat(start_date_str)
                end_date = datetime.fromisoformat(end_date_str)
                locations = locations.filter(timestamp__range=(start_date, end_date))
            except ValueError:
                pass

        if format == 'export':
            return ExcelDownload('sos', locations)

        page = self.paginate_queryset(locations)
        if page is not None:
            serializer = CustomerSosSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomerSosSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list_pending')
    def list_pending(self, request, *args, **kwargs):
        locations = CustomerSOS.objects.exclude(status=1).select_related('customer__user').order_by('id').all()
        serializer = CustomerSosPendingSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='close_sos')
    def close_sos(self, request, *args, **kwargs):
        try:
            data = request.data

            customer_id = data.get('customer')
            user_id = data.get('user')
            key = data.get('key')
            id = data.get('id')

            customer = Customer.objects.filter(id=customer_id, user=user_id).first()
            customerSOS = CustomerSOS.objects.filter(id=id, customer=customer, key=key).first()

            if customer is None or customerSOS is None:
                return Response({"message": "Customer not found"}, status=404)

            customerSOS.status = 1
            customerSOS.save()

            return Response({ "mgs": "OK" })
        except Exception as e:
            return Response({"message": str(e)}, status=400)


def ExcelDownload(type, queryset):
    if type == "sos":
        serializer = ExcelSerializer(data={ 'data': CustomerSosSerializer(queryset, many=True).data })
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.to_excel({
            'timestamp': 'Fecha/Hora',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
            'status': 'Atendido'
        }, {
            'status': 'boolean'
        })
    else:
        serializer = ExcelSerializer(data={ 'data': CustomerLocationSerializer(queryset, many=True).data })
        serializer.is_valid(raise_exception=True)
        excel_file = serializer.to_excel({
            'timestamp': 'Fecha/Hora',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
        }, { })

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    excel_file.save(response)
    return response