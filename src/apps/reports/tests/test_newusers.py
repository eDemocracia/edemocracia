import pytest
from mixer.backend.django import mixer
from apps.reports.models import NewUsersReport
from django.db import IntegrityError
from django.urls import reverse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class TestNewUsersReport():
    @pytest.mark.django_db
    def test_new_users_create(self):
        new_users = mixer.blend(NewUsersReport)
        assert NewUsersReport.objects.count() == 1
        assert new_users.__str__() == ('{} - {}').format(
            new_users.start_date.strftime("%d/%m/%Y"), new_users.period)

    @pytest.mark.django_db
    def test_new_users_integrity_error(self):
        content = mixer.blend(NewUsersReport)
        with pytest.raises(IntegrityError) as excinfo:
            mixer.blend(NewUsersReport,
                        period=content.period,
                        start_date=content.start_date)
        assert 'UNIQUE constraint failed' in str(
            excinfo.value)
        ## PostgreSQL message error
        # assert 'duplicate key value violates unique constraint' in str(
        #     excinfo.value)

    @pytest.mark.django_db
    def test_new_users_api_url(api_client):
        mixer.cycle(5).blend(NewUsersReport)
        url = reverse('newusersreport-list')
        client = APIClient()
        response = client.get(url)
        request = json.loads(response.content)

        assert response.status_code == 200
        assert request['count'] == 5
