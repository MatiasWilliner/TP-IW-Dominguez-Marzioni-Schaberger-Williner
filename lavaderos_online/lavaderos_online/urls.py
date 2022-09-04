
from django.contrib import admin
from django.urls import path, include
from lavaderos  import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('perfil/', views.perfil, name="perfil"),
    path('admin/', admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),
    path("register/", views.register_request, name="register"),
    path('lavaderos/', views.basic, name="lavaderos"),
    path('perfillavadero/<id>', views.lavadero, name="perfillavadero"),
    path('registrolavadero/', views.registroLavadero),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
