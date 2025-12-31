from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import CustomSearchFilter
from core.models import Company
from core.serializers.company import CompanySerializer
from core.permissions import IsAdminOrCustomerReadOnly

class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrCustomerReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, CustomSearchFilter]
    search_fields = ['name', 'NIT']

    @action(detail=False, methods=['get'])
    def lts(self, request):
        companies = Company.objects.filter(is_active=True).all()
        data = companies.values('id', 'name')
        return Response(data)