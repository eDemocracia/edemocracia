from django.contrib import admin
from apps.reports.models import NewUsersReport


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsersReport, NewUsersAdmin)
