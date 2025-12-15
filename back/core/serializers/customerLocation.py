from rest_framework import serializers

from core.models import CustomerLocation


class CustomerLocationSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")

    class Meta:
        model = CustomerLocation
        fields = '__all__'