from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument('recipient_email', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        recipient_email = options['recipient_email']
        
        subject = 'Test Email from Cars Empire'
        message = 'This is a test email from Cars Empire. If you receive this, the email configuration is working correctly.'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        try:
            send_mail(
                subject,
                message,
                from_email,
                [recipient_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent test email to {recipient_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}')) 