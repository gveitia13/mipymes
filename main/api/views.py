from rest_framework import viewsets, filters, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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
