from django.urls import include, path
from rest_framework import routers
from .ec_app import views

router = routers.DefaultRouter()
router.register(r'system', views.SystemViewSet)
router.register(r'report', views.ReportViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
