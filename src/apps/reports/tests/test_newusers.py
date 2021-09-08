import pytest
from mixer.backend.django import mixer
from apps.reports.models import NewUsersReport
from django.db import IntegrityError
from django.urls import reverse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.reports.tasks import (create_new_users_object,
                                get_new_users_daily,
                                get_new_users_monthly,
                                get_new_users_yearly)
import calendar


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

    def test_create_new_users_daily(self):
        data_daily = ['2020-11-23', 10]
        new_users_object = create_new_users_object(data_daily, 'daily')

        assert new_users_object.period == 'daily'
        assert new_users_object.start_date == '2020-11-23'
        assert new_users_object.end_date == '2020-11-23'
        assert new_users_object.new_users == 10

    @pytest.mark.django_db
    def test_create_new_users_monthly(self):
        data_monthly = {
            'month': date(2020, 1, 1),
            'total_registers': 10
        }

        new_users_object = create_new_users_object(data_monthly, 'monthly')

        assert new_users_object.period == 'monthly'
        assert new_users_object.start_date == date(2020, 1, 1)
        assert new_users_object.end_date == date(2020, 1, 31)
        assert new_users_object.new_users == 10

    @pytest.mark.django_db
    def test_create_new_users_yearly(self):
        data_yearly = {
            'year': date(2019, 1, 1),
            'total_registers': 10
        }

        new_users_object = create_new_users_object(data_yearly, 'yearly')

        assert new_users_object.period == 'yearly'
        assert new_users_object.start_date == date(2019, 1, 1)
        assert new_users_object.end_date == date(2019, 12, 31)
        assert new_users_object.new_users == 10

    @pytest.mark.django_db
    def test_get_new_users_daily_with_args(self):
        mixer.blend(get_user_model(), date_joined='2020-10-01')

        get_new_users_daily.apply(args=(['2020-10-01']))

        daily_data = NewUsersReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == date(2020, 10, 1)
        assert daily_data.end_date == date(2020, 10, 1)
        assert daily_data.period == 'daily'
        assert daily_data.new_users == 1

    @pytest.mark.django_db
    def test_get_new_users_daily_without_args(self):
        yesterday = datetime.now() - timedelta(days=1)
        mixer.blend(get_user_model(), date_joined=yesterday)

        get_new_users_daily.apply()

        daily_data = NewUsersReport.objects.filter(
            period='daily').first()

        assert daily_data.start_date == yesterday.date()
        assert daily_data.end_date == yesterday.date()
        assert daily_data.period == 'daily'
        assert daily_data.new_users == 1

    @pytest.mark.django_db
    def test_get_new_users_monthly_with_args(self):
        mixer.cycle(5).blend(NewUsersReport, period='daily',
                             new_users=10, start_date=mixer.sequence(
                                 '2020-10-1{0}'),
                             end_date=mixer.sequence('2020-10-1{0}'))

        get_new_users_monthly.apply(args=(['2020-10-01']))

        monthly_data = NewUsersReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == date(2020, 10, 1)
        assert monthly_data.end_date == date(2020, 10, 31)
        assert monthly_data.period == 'monthly'
        assert monthly_data.new_users == 50

    @pytest.mark.django_db
    def test_get_new_users_monthly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(NewUsersReport, period='daily', new_users=10,
                    start_date=yesterday, end_date=yesterday)

        get_new_users_monthly.apply()

        monthly_data = NewUsersReport.objects.filter(
            period='monthly').first()

        assert monthly_data.start_date == yesterday.replace(day=1)
        assert monthly_data.end_date == yesterday
        assert monthly_data.period == 'monthly'
        assert monthly_data.new_users == 10

    @pytest.mark.django_db
    def test_get_new_users_yearly_with_args(self):
        start_dates = ['2019-01-01', '2019-02-01', '2019-03-01']
        end_dates = ['2019-01-31', '2019-02-28', '2019-03-31']
        for i in range(3):
            mixer.blend(NewUsersReport, period='monthly', new_users=10,
                        start_date=start_dates[i], end_date=end_dates[i])

        get_new_users_yearly.apply(args=(['2019-01-01']))

        yearly_data = NewUsersReport.objects.filter(
            period='yearly').first()

        assert yearly_data.start_date == date(2019, 1, 1)
        assert yearly_data.end_date == date(2019, 12, 31)
        assert yearly_data.period == 'yearly'
        assert yearly_data.new_users == 30

    @pytest.mark.django_db
    def test_get_new_users_yearly_without_args(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(NewUsersReport, period='monthly', new_users=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)

        get_new_users_yearly.apply()

        yearly_data = NewUsersReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.new_users == 10

    @pytest.mark.django_db
    def test_get_new_users_yearly_current_year(self):
        yesterday = date.today() - timedelta(days=1)
        mixer.blend(NewUsersReport, period='monthly', new_users=10,
                    start_date=yesterday.replace(day=1),
                    end_date=yesterday)
        mixer.blend(NewUsersReport, period='yearly', new_users=9,
                    start_date=yesterday.replace(day=1, month=1),
                    end_date=yesterday - timedelta(days=1))

        get_new_users_yearly.apply()

        yearly_data = NewUsersReport.objects.filter(period='yearly').first()

        assert yearly_data.start_date == yesterday.replace(day=1, month=1)
        assert yearly_data.end_date == yesterday
        assert yearly_data.period == 'yearly'
        assert yearly_data.new_users == 10
