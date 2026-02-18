from rest_framework import serializers
from django.contrib.auth import get_user_model
from soslince.mixins.baseImage import BaseImageMixin
from core.models import Customer


class CustomerInfoSerializer(BaseImageMixin, serializers.ModelSerializer):
    url_image = BaseImageMixin.url_image
    company_name = serializers.CharField(source='company.name', read_only=True, allow_null=True)
    phone = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Customer
        exclude = ['user']

    def validate_phone(self, value):
        # Check if the phone number is unique among Customers. Exclude the
        # customer instance being updated so the same number can be kept.
        query = Customer.objects.filter(phone=value)

        # Try to determine the current Customer instance to exclude.
        customer_instance = getattr(self, 'instance', None)

        if customer_instance is None:
            parent = getattr(self, 'parent', None)
            user_instance = None
            if parent is not None:
                user_instance = getattr(parent, 'instance', None)
                # In some nesting shapes parent.parent holds the user serializer
                if user_instance is None:
                    grandparent = getattr(parent, 'parent', None)
                    user_instance = getattr(grandparent, 'instance', None) if grandparent is not None else None

            if user_instance is not None:
                customer_instance = getattr(user_instance, 'customer', None)

        if customer_instance is not None:
            query = query.exclude(pk=customer_instance.pk)

        if query.exists():
            raise serializers.ValidationError("Este número de teléfono ya está en uso.")

        return value


class MinimalCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name']


class CustomerSerializer(BaseImageMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    customer_info = CustomerInfoSerializer(source='customer')

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'password', 'customer_info']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        User = get_user_model()
        query = User.objects.filter(email=value)
        
        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
            
        return value

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

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.username = instance.email

        if password:
            instance.set_password(password)
        instance.save()

        # info_serializer = self.fields['customer_info']
        # info_serializer.instance = customer_instance
        # validated_customer_data = info_serializer.validate(customer_data)

        if customer_data:
            customer_instance, created = Customer.objects.get_or_create(user=instance)
            for attr, value in customer_data.items():
                setattr(customer_instance, attr, value)
            customer_instance.save()

        return instance