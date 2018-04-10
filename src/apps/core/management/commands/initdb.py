from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import re
import os
import sys


User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin and update site name'

    def handle(self, *args, **options):
        self.create_admin()
        self.update_site()

    def update_site(self):
        site = Site.objects.get_current()
        site_name = os.environ.get('SITE_NAME', None)
        site_url = os.environ.get('SITE_URL', None)

        if None not in [site_url, site_name]:
            print('Updating site infos...')
            regex = re.compile('^(http|https)://')
            for scheme in regex.findall(site_url):
                site_url = site_url.replace(scheme + '://', '')
            site.domain, site.name = site_url, site_name
            site.save()
            print('Done!')
        else:
            print('Missing SITE_URL or SITE_NAME environment variable.')
            sys.exit(2)

    def create_admin(self):
        admin_email = os.environ.get('ADMIN_EMAIL', None)
        admin_username = os.environ.get('ADMIN_USERNAME', None)
        admin_passwd = os.environ.get('ADMIN_PASSWORD', None)

        if None not in [admin_email, admin_passwd, admin_username]:
            print('Creating superuser...')
            user = User.objects.get_or_create(email=admin_email,
                                              username=admin_username)[0]
            user.set_password(admin_passwd)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print('Done!')
        else:
            print('Missing ADMIN_EMAIL, ADMIN_USERNAME or ADMIN_PASSWORD '
                  'environment variable.')
            sys.exit(1)
