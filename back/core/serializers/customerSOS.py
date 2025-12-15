from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Customer, CustomerSOS


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'is_active', 'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'image', 'blood_type', 'company', 'birth_date', 'secret_word', 'details']


class CustomerSosSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    class Meta:
        model = CustomerSOS
        fields = '__all__'


class CustomerSosPendingSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    customer = CustomerSerializer()

    class Meta:
        model = CustomerSOS
        fields = '__all__'