from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import json


class Command(BaseCommand):
    help = 'Load existing users from edemocracia-colab'

    def handle(self, *args, **options):
        path = options['pythonpath']
        with open(path, 'r') as json_file:
            data = json.loads(json_file.read())
        for user in data:
            self._import_user(user['fields'], user['pk'])

    def _import_user(self, user_data, user_id):
        user, created = User.objects.update_or_create(
            defaults={
                'id': user_id,
                'username': user_data['username'],
                'email': user_data['email']
            },
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_active=user_data['is_active'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser'],
            date_joined=user_data['date_joined'],
            last_login=user_data['last_login'])

        if created:
            print("%s has been created" % user.username)
        else:
            print("%s already exists" % user.username)
