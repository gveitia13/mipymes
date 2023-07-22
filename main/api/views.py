import json

from coreapi.compat import force_text
from django.db.models import Q, F, Func
from django.db.models.functions import Lower
from rest_framework import viewsets, filters, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from unidecode import unidecode

from main.api.pagination import EnterprisePaginator
from main.api.serializers import EnterpriseSerializer, SectorSerializer, EnlaceSerializer, ServiceSerializer, \
    PublicidadSerializer, ProvinciaSerializer, MunicipioSerializer, PublicidadGeneralSerializer, ContactoSerializer
from main.models import Enterprise, Sector, Enlace, Service, Publicidad, Provincia, Municipio, PublicidadGeneral, \
    Contacto


class Unidecode(Func):
    function = 'REPLACE'
    template = "UNIDECODE(LOWER(%(expressions)s))"


class EnterpriseVS(viewsets.ModelViewSet):
    queryset = Enterprise.objects.filter(is_active=True, )
    serializer_class = EnterpriseSerializer
    pagination_class = EnterprisePaginator
    filter_backends = [filters.OrderingFilter, ]
    ordering_fields = ['nombre', 'is_active', 'fecha_aprobacion']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('provincia'):
            queryset = queryset.filter(municipio__provincia_id=self.request.query_params.get('provincia'))
        if self.request.query_params.get('municipio'):
            queryset = queryset.filter(municipio_id=self.request.query_params.get('municipio'))
        if self.request.query_params.get('sector'):
            queryset = queryset.filter(sectores__in=self.request.query_params.get('sector'))
        if self.request.query_params.get('search'):
            search_query = self.request.query_params.get('search', None)
            search_terms = search_query.split(' ')
            for search_term in search_terms:
                search_term = unidecode(force_text(search_term)).lower()
                listado = list(filter(lambda e: str(e.get_nombre_al_berro()).__contains__(search_term), queryset))
                claves_primarias = [obj.pk for obj in listado]
                queryset = queryset.filter(pk__in=claves_primarias)
        return queryset


class SectorVS(viewsets.ReadOnlyModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class EnlaceVS(viewsets.ModelViewSet):
    queryset = Enlace.objects.all()
    serializer_class = EnlaceSerializer


class ServiceVS(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class PublicidadVS(viewsets.ReadOnlyModelViewSet):
    queryset = Publicidad.objects.all()
    serializer_class = PublicidadSerializer


class ContactoVS(viewsets.ReadOnlyModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer


class PublicidadGeneralVS(viewsets.ReadOnlyModelViewSet):
    queryset = PublicidadGeneral.objects.all()
    serializer_class = PublicidadGeneralSerializer


class ProvinciaVS(viewsets.ReadOnlyModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class MunicipioVS(viewsets.ReadOnlyModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer


class AssignSectorAV(APIView):
    def put(self, request: Request, pk):
        try:
            enterprise = Enterprise.objects.get(pk=pk)
            de_serializer = SectorSerializer(data=request.data, many=True)
            if de_serializer.is_valid():
                print('')

            for s in enterprise.sectores.all():
                enterprise.sectores.remove(s)

            for sector in de_serializer.data:
                dict_sector = dict(sector)
                if dict_sector.get('id'):
                    enterprise.sectores.add(Sector.objects.get(pk=dict_sector.get('id')))
                else:
                    try:
                        s = Sector.objects.create(sector=dict_sector.get('sector'))
                        enterprise.sectores.add(s)
                    except:
                        return Response({'error': 'Ya existe un sector con este nombre'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(EnterpriseSerializer(instance=enterprise).data, status=status.HTTP_200_OK)
        except Enterprise.DoesNotExist:
            return Response({'error': f'No se encontró empresa con id {pk}'}, status=status.HTTP_404_NOT_FOUND)
