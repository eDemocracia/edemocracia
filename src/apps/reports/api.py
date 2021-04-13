from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, filters
from apps.reports.models import NewUsersReport
from apps.reports.serializers import NewUsersSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class NewUsersFilter(FilterSet):
    class Meta:
        model = NewUsersReport
        fields = {
            'start_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'end_date': ['lt', 'lte', 'gt', 'gte', 'year', 'month'],
            'period': ['exact'],
        }


class NewUsersViewSet(viewsets.ReadOnlyModelViewSet):
    allowed_methods = ['get']
    queryset = NewUsersReport.objects.all()
    serializer_class = NewUsersSerializer
    filter_class = NewUsersFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = '__all__'

    @method_decorator(cache_page(1)) # 1 minute
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['sum_total_results'] = sum([data.get('new_users', 0)
            for data in response.data['results']])
        return response


@api_view(['GET'])
def api_reports_root(request, format=None):
    return Response({
        'newusers': reverse('newusersreport-list',
                            request=request, format=format),
    })
