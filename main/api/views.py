from rest_framework import generics, viewsets, filters

from main.api.pagination import EnterprisePaginator
from main.api.serializers import EnterpriseSerializer, SectorSerializer, EnlaceSerializer, ServiceSerializer, \
    PublicidadSerializer, ProvinciaSerializer, MunicipioSerializer
from main.models import Enterprise, Sector, Enlace, Service, Publicidad, Provincia, Municipio


class EnterpriseVS(viewsets.ModelViewSet):
    queryset = Enterprise.objects.filter(is_active=True)
    serializer_class = EnterpriseSerializer
    pagination_class = EnterprisePaginator
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, ]
    search_fields = ['nombre', 'representante']
    ordering_fields = ['nombre', 'is_active', 'fecha_aprobacion']


class SectorVS(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class EnlaceVS(viewsets.ModelViewSet):
    queryset = Enlace.objects.all()
    serializer_class = EnlaceSerializer


class ServiceVS(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class PublicidadVS(viewsets.ModelViewSet):
    queryset = Publicidad.objects.all()
    serializer_class = PublicidadSerializer


class ProvinciaVS(viewsets.ReadOnlyModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class MunicipioVS(viewsets.ReadOnlyModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
