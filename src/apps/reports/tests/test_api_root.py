import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.urls import reverse
import json


@pytest.mark.django_db
def test_reports_api_root_url():
    url = reverse('reports_api_root')
    client = APIClient()
    response = client.get(url)
    request = json.loads(response.content)

    assert response.status_code == 200
