from rest_framework import serializers
from django.contrib.auth import get_user_model
from soslince.mixins.baseImage import BaseImageMixin
from core.models import Staff


class StaffInfoSerializer(BaseImageMixin, serializers.ModelSerializer):
    url_image = BaseImageMixin.url_image
    phone = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Staff
        fields = ['phone', 'image', 'url_image']

    def validate_phone(self, value):
        query = Staff.objects.filter(phone=value)

        # Determine current staff instance (either this serializer's instance
        # or via the parent user serializer) so we can exclude it on update.
        staff_instance = getattr(self, 'instance', None)

        if staff_instance is None:
            parent = getattr(self, 'parent', None)
            user_instance = None
            if parent is not None:
                user_instance = getattr(parent, 'instance', None)
                if user_instance is None:
                    grandparent = getattr(parent, 'parent', None)
                    user_instance = getattr(grandparent, 'instance', None) if grandparent is not None else None

            if user_instance is not None:
                staff_instance = getattr(user_instance, 'staff', None)

        if staff_instance is not None:
            query = query.exclude(pk=staff_instance.pk)

        if query.exists():
            raise serializers.ValidationError("This phone number is already in use.")

        return value

class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(source='staff.phone', read_only=True)
    staff_info = StaffInfoSerializer(source='staff')

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'password', 'phone', 'staff_info']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        User = get_user_model()
        query = User.objects.filter(email=value)

        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def create(self, validated_data):
        staff_data = validated_data.pop('staff', None)

        validated_data['is_staff'] = True
        validated_data['username'] = validated_data['email']
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()

        if staff_data:
            Staff.objects.create(user=user, **staff_data)

        return user

    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff', None)

        if not self.context['request'].user.is_superuser:
            validated_data.pop('is_superuser', None)

        password = validated_data.pop('password', None)
        validated_data.pop('email', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        if staff_data:
            staff_instance, created = Staff.objects.get_or_create(user=instance)
            for attr, value in staff_data.items():
                setattr(staff_instance, attr, value)
            staff_instance.save()

        return instance

class StaffListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='staff.image', read_only=True)
    phone = serializers.CharField(source='staff.phone', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'is_active', 'is_superuser', 'image',]
