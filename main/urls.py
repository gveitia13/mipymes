from django.urls import path

from main.views import cargar_empresas, cargar_sectores, cargar_provincias

urlpatterns = [
    path('cargar_empresas/', cargar_empresas, name='cargar-empresas'),
    path('cargar_sectores/', cargar_sectores, name='cargar_sectores'),
    path('cargar_provincias/', cargar_provincias, name='cargar-provincias'),
]
