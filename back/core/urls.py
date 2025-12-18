from rest_framework import routers
from django.urls import path

from .viewsets.customer import CustomerViewSet
from .viewsets.staff import StaffViewSet
from .viewsets.company import CompanyViewSet

from .apiview.user import UserAPIView
from .apiview.test import TestAPIView

router = routers.SimpleRouter()
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'company', CompanyViewSet, basename='company')

urlpatterns = router.urls + [
    path('user/data/', UserAPIView.as_view(), name='get-user-data'),
    path('test/', TestAPIView.as_view(), name='get-test'),
]