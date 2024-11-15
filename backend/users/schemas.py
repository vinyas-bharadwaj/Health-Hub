from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from .serializers import PatientRegisterSerializer

user_list_docs = extend_schema(
    responses=PatientRegisterSerializer(),
    parameters=[
        OpenApiParameter(
            name="Username",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Username",
        ),
        OpenApiParameter(
            name="Email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Email",
        ),
        OpenApiParameter(
            name="Password",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Password",
        ),
    ]
)