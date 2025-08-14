# CÓDIGO CORRIGIDO

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rotas corrigidas sem a barra invertida
    path('admin/', admin.site.urls),
    path('api/', include('inspetoria_app.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]

# Esta linha já estava correta, mas a mantemos aqui
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
