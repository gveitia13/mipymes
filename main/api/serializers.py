from django.core.mail import send_mail
from django.forms import model_to_dict
from rest_framework import serializers

from main.models import Enterprise, Sector, Service, Enlace, Publicidad, Provincia, Municipio, PublicidadGeneral, \
    Config, Contacto
from mipymes import settings


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


class PublicidadGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicidadGeneral
        fields = '__all__'


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    municipios = MunicipioSerializer(many=True, allow_null=True, required=False, )

    class Meta:
        model = Provincia
        fields = '__all__'


class EnterpriseSerializer(serializers.ModelSerializer):
    sectores = SectorSerializer(many=True, allow_null=True, required=False, read_only=True)
    servicios = ServiceSerializer(many=True, allow_null=True, required=False, read_only=True)
    enlaces = EnlaceSerializer(many=True, allow_null=True, required=False, read_only=True)
    publicidades = PublicidadSerializer(many=True, allow_null=True, required=False, read_only=True)
    municipio_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False, )
    provincia_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False)

    def create(self, validated_data):
        a = super().create(validated_data)
        if Config.objects.exists():
            try:
                send_mail('Nueva empresa desde la APP',
                          f'La empresa "{validated_data["nombre"]}" ha sido creada desde la APP',
                          settings.EMAIL_HOST_USER,
                          [Config.objects.first().email])
            except Exception as e:
                print('Explotó el correo. Excepción: ' + str(e))
        return a

    def get_municipio_object(self, object):
        serializer = MunicipioSerializer(instance=object.municipio).data
        return serializer

    def get_provincia_object(self, object):
        return model_to_dict(object.municipio.provincia)

    class Meta:
        model = Enterprise
        fields = '__all__'
