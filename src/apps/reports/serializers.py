from rest_framework import serializers
from apps.reports.models import NewUsersReport


class NewUsersSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    modified = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    def get_month(self, obj):
        return obj.start_date.month

    def get_year(self, obj):
        return obj.start_date.year

    class Meta:
        model = NewUsersReport
        fields = ('start_date', 'end_date', 'period', 'new_users', 'month',
                  'year', 'modified')
