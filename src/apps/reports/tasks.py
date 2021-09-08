from edemocracia import celery_app
from django.contrib.auth import get_user_model
from apps.reports.models import NewUsersReport
from collections import Counter
from datetime import timedelta
import calendar
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from django.utils import timezone


def create_new_users_object(registers_by_date, period='daily'):
    yesterday = timezone.now().date() - timedelta(days=1)

    if period == 'daily':
        registers_count = registers_by_date[1]
        start_date = end_date = registers_by_date[0]

    else:
        registers_count = registers_by_date['total_registers']

        if period == 'monthly':
            start_date = registers_by_date['month']
            if (start_date.year == yesterday.year and
                start_date.month == yesterday.month):
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                last_day = calendar.monthrange(start_date.year,
                                               start_date.month)[1]
                end_date = start_date.replace(day=last_day)

        elif period == 'yearly':
            start_date = registers_by_date['year']
            if start_date.year == yesterday.year:
                end_date = yesterday.strftime('%Y-%m-%d')
            else:
                end_date = start_date.replace(day=31, month=12)

        if NewUsersReport.objects.filter(
            start_date=start_date, period=period).exists():
            NewUsersReport.objects.filter(
                start_date=start_date, period=period).delete()

    report_object = NewUsersReport(start_date=start_date, end_date=end_date,
                                   new_users=registers_count, period=period)
    return report_object


@celery_app.task(name="get_new_users_daily")
def get_new_users_daily(start_date=None):
    batch_size = 100
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=23, minute=59, second=59)

    if not start_date:
        start_date = yesterday.replace(
            hour=0, minute=0, second=0, microsecond=0)

    users = get_user_model().objects.filter(date_joined__gte=start_date,
                                            date_joined__lte=yesterday)

    date_joined_list = [user.date_joined.strftime('%Y-%m-%d')
                        for user in users]

    registers_by_day = Counter(date_joined_list)

    registers_daily = [create_new_users_object(result, 'daily')
                       for result in registers_by_day.items()]

    NewUsersReport.objects.bulk_create(registers_daily, batch_size)


@celery_app.task(name="get_new_users_monthly")
def get_new_users_monthly(start_date=None):
    batch_size = 100
    end_date = timezone.now().date()

    if not start_date:
        start_date = end_date.replace(day=1).strftime('%Y-%m-%d')

    registers_daily = NewUsersReport.objects.filter(
        period='daily',
        start_date__gte=start_date,
        end_date__lte=end_date.strftime('%Y-%m-%d'))

    data_by_month = registers_daily.annotate(
        month=TruncMonth('start_date')).values('month').annotate(
            total_registers=Sum('new_users')).values(
                'month', 'total_registers')

    registers_monthly = [create_new_users_object(result, 'monthly')
                         for result in data_by_month]

    NewUsersReport.objects.bulk_create(registers_monthly, batch_size)


@celery_app.task(name="get_new_users_yearly")
def get_new_users_yearly(start_date=None):
    batch_size = 100
    today = timezone.now().date()
    last_day = calendar.monthrange(today.year, today.month)[1]

    if not start_date:
        start_date = today.replace(day=1, month=1).strftime('%Y-%m-%d')

    registers_monthly = NewUsersReport.objects.filter(
        period='monthly',
        start_date__gte=start_date,
        end_date__lte=today.replace(day=last_day).strftime('%Y-%m-%d'))

    data_by_year = registers_monthly.annotate(
        year=TruncYear('start_date')).values('year').annotate(
            total_registers=Sum('new_users')).values(
                'year', 'total_registers')

    registers_yearly = [create_new_users_object(result, 'yearly')
                        for result in data_by_year]

    NewUsersReport.objects.bulk_create(registers_yearly, batch_size)
