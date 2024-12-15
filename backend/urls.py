from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Міні-склад",
      default_version='v1',
      description="Документація API",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@yourapi.local"),
      # license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/',include('users.urls',namespace='users')),
    path('inventory/', include('inventory.urls',namespace='inventory')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
