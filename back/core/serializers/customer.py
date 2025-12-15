from rest_framework import serializers
from django.contrib.auth import get_user_model
from soslince.mixins.baseImage import BaseImageMixin
from core.models import Customer


class CustomerInfoSerializer(BaseImageMixin, serializers.ModelSerializer):
    url_image = BaseImageMixin.url_image

    class Meta:
        model = Customer
        exclude = ['user']

class CustomerSerializer(BaseImageMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    customer_info = CustomerInfoSerializer(source='customer')

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'password', 'customer_info']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        customer_data = validated_data.pop('customer', None)

        validated_data['username'] = validated_data['email']
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()

        if customer_data:
            Customer.objects.create(user=user, **customer_data)

        return user

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer', None)

        password = validated_data.pop('password', None)
        validated_data.pop('email', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        if customer_data:
            customer_instance, created = Customer.objects.get_or_create(user=instance)
            for attr, value in customer_data.items():
                setattr(customer_instance, attr, value)
            customer_instance.save()

        return instance