from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main.api.views import EnterpriseVS, SectorVS, EnlaceVS, ServiceVS, PublicidadVS, ProvinciaVS, MunicipioVS

router = DefaultRouter()
router.register('empresa', EnterpriseVS, basename='empresa')
router.register('sector', SectorVS, basename='sector')
router.register('enlace', EnlaceVS, basename='enlace')
router.register('servicio', ServiceVS, basename='servicio')
router.register('publicidad', PublicidadVS, basename='publicidad')
router.register('provincia', ProvinciaVS, basename='provincia')
router.register('municipio', MunicipioVS, basename='municipio')

urlpatterns = [
    path('', include(router.urls)),
]
