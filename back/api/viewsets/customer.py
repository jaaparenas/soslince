from datetime import datetime, timezone

from rest_framework import viewsets, mixins, views
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from core.models import Customer, CustomerSOS, CustomerLocation, Company
from soslince.mixins.baseImage import BaseImageMixin

class CustomerViewSet(viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    @action(detail=False, methods=['get'], url_path='data')
    def data(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        customer = Customer.objects.filter(user=user).first()
        if not customer:
            return Response({"message": "Customer not found"}, status=404)

        data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": customer.image if customer else "",
            "phone": customer.phone if customer else "",
            "blood_type": customer.blood_type if customer else 1,
            "company": customer.company.id if customer and customer.company else None,
            "birth_date": customer.birth_date if customer else "",
            "secret_word": customer.secret_word if customer else "",
            "details": customer.details if customer else "",
        }

        return Response(data)


    @action(detail=False, methods=['post'], url_path='sos')
    def sos(self, request):

        if request.user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        data = request.data
        key = data.get('key')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or latitude == 0 or \
            longitude is None or longitude == 0 or \
            key is None or key == "":
                return Response({"message": "Missing parameters"}, status=400)

        customer = Customer.objects.filter(user=request.user.id).first()
        customerSOS = CustomerSOS.objects.filter(key=key, customer=customer).first()
        if customerSOS is None:
            customerSOS = CustomerSOS()

        customerSOS.customer = customer
        customerSOS.latitude = latitude
        customerSOS.longitude = longitude
        customerSOS.key = key
        customerSOS.save()

        return Response({ "mgs": key }, status=200)


    @action(detail=False, methods=['post'], url_path='location')
    def location(self, request):
        if request.user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        data = request.data
        latitude = data.get('location', {}).get('coords', {}).get('latitude')
        longitude = data.get('location', {}).get('coords', {}).get('longitude')
        timestamp_str = data.get('location', {}).get('timestamp')

        if not latitude or not longitude or not timestamp_str:
            return Response({"message": "Missing parameters"}, status=400)

        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return Response({"message": "Customer not found"}, status=404)

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError:
            return Response({"message": "Invalid timestamp format"}, status=400)

        last_location = CustomerLocation.objects.filter(customer=customer).order_by('-timestamp').first()

        if last_location:
            last_timestamp = last_location.timestamp

            timestamp = timestamp.astimezone(last_timestamp.tzinfo)
            time_diff = (timestamp - last_timestamp).total_seconds()
            if time_diff < 60:
                return Response({"message": "Location update too frequent"}, status=200)

        CustomerLocation.objects.create(
            customer=customer,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp
        )

        return Response({"message": "OK"}, status=200)


    @action(detail=False, methods=['post'], url_path='profile')
    def profile(self, request):

        if request.user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        try:
            user = get_user_model().objects.get(id=request.user.id)
            customer = Customer.objects.filter(user=request.user.id).first()

            if user is None or customer is None:
                return Response({"message": "Customer not found"}, status=404)

            data = request.data

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            birth_date = data.get('birth_date')
            blood_type = data.get('blood_type')
            company = data.get('company')
            secret_word = data.get('secret_word')
            details = data.get('details')
            url_image = data.get('url_image')

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone:
                customer.phone = phone
            if birth_date:
                customer.birth_date = birth_date
            if blood_type:
                customer.blood_type = blood_type
            if company is not None and company != "":
                company_obj = None
                # Accept numeric id (int or numeric string)
                try:
                    if isinstance(company, (int, str)) and str(company).isdigit():
                        company_obj = Company.objects.filter(id=int(company)).first()
                    elif isinstance(company, dict) and company.get('id'):
                        company_obj = Company.objects.filter(id=company.get('id')).first()
                    elif isinstance(company, Company):
                        company_obj = company
                except Exception:
                    company_obj = None

                # Assign Company instance or None to avoid assignment errors
                customer.company = company_obj
            if secret_word:
                customer.secret_word = secret_word
            if details:
                customer.details = details
            if url_image:
                if url_image.startswith('data:image/') and len(url_image) > 100:
                    customer.image = BaseImageMixin.save_image(self, url_image)

            customer.save()
            user.save()

            return Response({ "mgs": "OK" }, status=200)

        except Exception as e:
            return Response({"message": str(e)}, status=400)


    @action(detail=False, methods=['post'], url_path='password')
    def password(self, request):

        if request.user.is_anonymous:
            return Response({"message": "Unauthorized"}, status=401)

        try:
            user = get_user_model().objects.get(id=request.user.id)
            customer = Customer.objects.filter(user=request.user.id).first()

            if user is None or customer is None:
                return Response({"message": "Customer not found"}, status=404)

            data = request.data

            password = data.get('password')

            if password is None or password == "":
                return Response({"message": "Missing parameters"}, status=400)

            user.set_password(data.get('password'))
            user.save()

            return Response({ "mgs": "OK" }, status=200)

        except Exception as e:
            return Response({"message": str(e)}, status=400)