from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from soslince.utils.send_mails import send_email_from_template
from soslince.excel_serializer import ExcelSerializer
from core.models import Customer, CustomerLocation
import io
from datetime import date

@shared_task(name='Send daily report email')
def send_daily_report_email():
    excel_stream = None
    try:
        # 1. Query the data for active users
        User = get_user_model()
        active_users = User.objects.filter(is_active=True, is_staff=False).select_related('customer__company')

        report_data = []
        today = date.today()

        for user in active_users:
            # Calculate age
            age = None
            if hasattr(user, 'customer') and user.customer.birth_date:
                birth_date = user.customer.birth_date
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            # Get last location timestamp
            last_location = None
            if hasattr(user, 'customer'):
                last_location_obj = CustomerLocation.objects.filter(customer=user.customer).order_by('-timestamp').first()
                if last_location_obj:
                    last_location = last_location_obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

            report_data.append({
                'company': user.customer.company.name if hasattr(user, 'customer') and user.customer.company else 'N/A',
                'name': f"{user.first_name} {user.last_name}",
                'age': age if age is not None else 'N/A',
                'gender': user.customer.get_gender_display() if hasattr(user, 'customer') and user.customer.gender else 'N/A',
                'last_location_date': last_location if last_location else 'N/A',
            })

        # 2. Create the Excel file and prepare the email
        data_email = {
            'subject': 'Daily Active Users Report',
            'html_template': 'emails/daily_active_users_report.html',
            'message': '',
            'context': {
                'report_date': timezone.now().strftime('%Y-%m-%d'),
                'current_year': timezone.now().year,
            },
            'recipient_list': [settings.ADMIN_EMAIL],
            'attachments': []
        }

        if report_data:
            serializer = ExcelSerializer(data={'data': report_data})
            serializer.is_valid(raise_exception=True)
            
            map_headers = {
                'company': 'Company',
                'name': 'Name',
                'age': 'Age',
                'gender': 'Gender',
                'last_location_date': 'Last Location Date'
            }
            
            workbook = serializer.to_excel(map_headers)
            
            excel_stream = io.BytesIO()
            workbook.save(excel_stream)
            excel_stream.seek(0)
            
            excel_stream.name = f"daily_report_{timezone.now().strftime('%Y-%m-%d')}.xlsx"
            excel_stream.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            data_email['attachments'].append(excel_stream)

        # 3. Send the email
        send_email_from_template(**data_email)

    finally:
        # 4. Ensure the stream is closed
        if excel_stream:
            excel_stream.close()