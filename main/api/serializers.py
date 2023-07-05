from django.forms import model_to_dict
from rest_framework import serializers

from main.models import Enterprise, Sector, Service, Enlace, Publicidad, Provincia, Municipio


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class EnlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enlace
        fields = '__all__'


class PublicidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicidad
        fields = '__all__'


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    municipios = MunicipioSerializer(many=True, allow_null=True, required=False, )

    class Meta:
        model = Provincia
        fields = '__all__'


class EnterpriseSerializer(serializers.ModelSerializer):
    sectores = SectorSerializer(many=True, allow_null=True, required=False)
    servicios = ServiceSerializer(many=True, allow_null=True, required=False, )
    enlaces = EnlaceSerializer(many=True, allow_null=True, required=False)
    publicidades = PublicidadSerializer(many=True, allow_null=True, required=False)
    municipio_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False)
    # provincia = serializers.CharField(source='municipio.provincia')
    provincia_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False)

    def get_municipio_object(self, object):
        serializer = MunicipioSerializer(instance=object.municipio).data
        return serializer

    def get_provincia_object(self, object):
        return model_to_dict(object.municipio.provincia)

    class Meta:
        model = Enterprise
        fields = '__all__'
