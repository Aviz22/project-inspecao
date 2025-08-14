# inspetoria_app/urls.py
from django.urls import path
from .views import InspecaoDadosView, DadosBrutosInspecao

urlpatterns = [
    path('dados/', InspecaoDadosView.as_view(), name='dados-inspecao'),
    path('dados-brutos/', DadosBrutosInspecao.as_view(), name='dados-brutos-inspecao'),
]