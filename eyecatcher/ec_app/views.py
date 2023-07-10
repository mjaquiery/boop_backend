from drf_spectacular.utils import extend_schema_view, extend_schema

from .serializers import System, \
    SystemSerializer, \
    CreateSystemSerializer, \
    Report, \
    ReportSerializer
from rest_framework import viewsets
from .permissions import OwnSystemOrReadOnly

# Create your views here.


@extend_schema_view(
    list=extend_schema(
        summary="View all Systems",
        description="""
Systems are sources of data, i.e. a player running the Boop-Boop game in a browser.
        """
    ),
    retrieve=extend_schema(
        summary="View a single System"
    ),
    create=extend_schema(
        summary="Create a System",
        description="""
Systems are created with a set of properties, which are used to identify the system.
These properties are sent to the API when the system is created, and whenever the system reports.
        """,
        request=CreateSystemSerializer(),
        responses={201: CreateSystemSerializer()}
    )
)
class SystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows systems to be viewed or edited.
    """
    queryset = System.objects.all().order_by('id')
    permission_classes = [OwnSystemOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateSystemSerializer
        return SystemSerializer


@extend_schema_view(
    list=extend_schema(
        summary="View all Reports",
        description="""
Reports are data from a single click of the Boop-Boop game. They will contain the coordinates of the click and a
base64-encoded image from the webcam.
        """
    ),
    retrieve=extend_schema(
        summary="View a single Report"
    ),
    create=extend_schema(
        summary="Create a Reports",
        description="""
Reports are created by the Boop-Boop game when the player clicks. They will contain the coordinates of the click and a
base64-encoded image from the webcam.

They are sent to the server with an auth_code and a set of properties. 
These are used to identify the system that sent the report.
        """
    )
)
class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reports to be viewed or edited.
    """
    queryset = Report.objects.all().order_by('id')
    serializer_class = ReportSerializer
    permission_classes = [OwnSystemOrReadOnly]
