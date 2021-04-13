from django.urls import path
from apps.reports import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/new-users', api.NewUsersViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('api/', api.api_reports_root, name='reports_api_root'),
]
