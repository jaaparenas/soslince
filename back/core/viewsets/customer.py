from datetime import datetime
from django.utils import timezone
from datetime import datetime, timezone as py_timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Customer, CustomerLocation, CustomerSOS
from core.serializers.customer import CustomerSerializer, MinimalCustomerSerializer
from core.serializers.customerLocation import CustomerLocationSerializer
from core.serializers.customerSOS import CustomerSosSerializer, CustomerSosPendingSerializer
from core.filters import CustomSearchFilter

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
    filter_backends = [DjangoFilterBackend, CustomSearchFilter]
    filterset_fields = ['customer__company', 'customer__gender']
    search_fields = ['first_name', 'last_name']

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

    @action(detail=False, methods=['get'], url_path='last_locations')
    def last_locations(self, request, *args, **kwargs):
        # 1. Start with all active customers
        customers = Customer.objects.filter(user__is_active=True)

        # 2. Apply filters to customers
        customer_filters = {}
        
        company_ids_str = request.query_params.get('customer__company__in')
        if company_ids_str:
            customer_filters['company__id__in'] = [int(x) for x in company_ids_str.split(',')]
        
        gender_ids_str = request.query_params.get('customer__customer_info__gender__in')
        if gender_ids_str:
            customer_filters['gender__in'] = gender_ids_str.split(',')
            
        blood_type_ids_str = request.query_params.get('customer__customer_info__blood_type__in')
        if blood_type_ids_str:
            customer_filters['blood_type__in'] = blood_type_ids_str.split(',')
            
        birth_date_gte_str = request.query_params.get('customer__customer_info__birth_date__gte')
        if birth_date_gte_str:
            customer_filters['birth_date__gte'] = birth_date_gte_str
            
        birth_date_lte_str = request.query_params.get('customer__customer_info__birth_date__lte')
        if birth_date_lte_str:
            customer_filters['birth_date__lte'] = birth_date_lte_str

        if customer_filters:
            customers = customers.filter(**customer_filters)

        # 3. Handle timestamp__range for locations
        timestamp_range_str = request.query_params.get('timestamp__range')
        location_filters = {}
        if timestamp_range_str:
            try:
                start_date_str, end_date_str = timestamp_range_str.split(',')
                # Ensure timezone awareness for comparison
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                location_filters['timestamp__range'] = (start_date, end_date)
            except ValueError:
                pass # Ignore invalid date range

        customers_with_last_location = []

        for customer in customers.select_related('company', 'user'):
            # Get the last location for each customer, applying timestamp filter if present
            last_location_queryset = CustomerLocation.objects.filter(customer=customer)
            if location_filters:
                last_location_queryset = last_location_queryset.filter(**location_filters)

            last_location = last_location_queryset.order_by('-timestamp').first()

            if last_location:
                customers_with_last_location.append({
                    'customer': MinimalCustomerSerializer(customer.user).data,
                    'latitude': last_location.latitude,
                    'longitude': last_location.longitude,
                    'timestamp': last_location.timestamp
                })
        return Response(customers_with_last_location)

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