
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
    path("cuentas/", include("django.contrib.auth.urls"), name="cuentas"),
    path("register/", views.register_request, name="register"),
    path('lavaderos/', views.basic, name="lavaderos"),
    path('perfillavadero/<id>', views.lavadero, name="perfillavadero"),
    path('registrolavadero/', views.registroLavadero, name='registrolavadero'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('milavadero/', views.miLavadero, name="milavadero"),
    path('solicitudeslavado/', views.solicitudLavado, name="solicitudeslavado"),
    path('cambiar_estado_lavadero/', views.cambiarEstadoLavadero, name='cambiar-estado-lavadero'),
    path('search/', include('haystack.urls'), name="search"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
