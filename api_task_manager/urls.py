from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

#
# schema_view = get_schema_view(
#    openapi.Info(
#       title="API_task_manager",
#       default_version='v1',
#       description="Test task",
#       contact=openapi.Contact(email="ivanzorya@gmail.com"),
#       license=openapi.License(name="test license"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )
#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path(
    #     'swagger/',
    #     schema_view.with_ui('swagger', cache_timeout=0),
    #     name='schema-swagger-ui'
    # ),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'),
         name='redoc')
]
