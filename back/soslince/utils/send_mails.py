from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

def send_email_from_template(**data_email):
    from_email = settings.EMAIL_SENDER
    recipient_list = data_email.get('recipient_list', [])
    subject = data_email.get('subject', '')

    # HTML render
    html_template = data_email.get('html_template')
    html_content = ''
    if html_template:
        template = get_template(html_template)
        html_content = template.render(data_email.get('context', {}))

    msg = EmailMultiAlternatives(
        subject=subject,
        body=data_email.get('message', ''),
        from_email=from_email,
        to=recipient_list
    )

    # Add HTML
    if html_content:
        msg.attach_alternative(html_content, "text/html")

    # ✨ Add attachments
    attachments = data_email.get('attachments', [])
    for f in attachments:
        msg.attach(f.name, f.read(), f.content_type)


    msg.send()