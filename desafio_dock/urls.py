from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Dock Challenge API",
      default_version='v1',
      description="Documentação da API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="filipenascimentocub@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
