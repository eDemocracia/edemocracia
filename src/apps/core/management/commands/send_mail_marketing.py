from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.template.loader import render_to_string


User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--emails',
            type=str,
            help="Text file containing a list of emails (one email per line')"
        )

    def handle(self, *args, **options):
        emails = self.get_emails_list(options['emails'])
        subject = "Nova ferramenta no e-Democracia!"
        html = render_to_string('emails/mail_marketing.html',
                                {'domain': Site.objects.get_current().domain})
        for email in emails:
            print(email)
            mail = EmailMultiAlternatives(subject=subject, to=[email, ])
            mail.attach_alternative(html, 'text/html')
            mail.send()

    def get_emails_list(self, emails_filename):
        if emails_filename:
            emails_list = self.get_email_from_file(emails_filename)
        else:
            emails_list = list(
                User.objects.all().values_list('email', flat=True)
            )
        return filter(None, emails_list)

    def get_email_from_file(self, filename):
        with open(filename) as f:
            emails_list = f.readlines()

        return [x.strip() for x in emails_list]
