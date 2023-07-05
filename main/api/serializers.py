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
    sectores = SectorSerializer(many=True, allow_null=True, required=False,)
    servicios = ServiceSerializer(many=True, allow_null=True, required=False, read_only=True)
    enlaces = EnlaceSerializer(many=True, allow_null=True, required=False, read_only=True)
    publicidades = PublicidadSerializer(many=True, allow_null=True, required=False, read_only=True)
    municipio_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False)
    # provincia = serializers.CharField(source='municipio.provincia')
    provincia_object = serializers.SerializerMethodField(read_only=True, allow_null=True, required=False)

    def create(self, validated_data):
        sectores_data = validated_data.pop('sectores')
        enterprise = Enterprise.objects.create(**validated_data)
        for sector in sectores_data:
            s = Sector.objects.create(**sector)
            enterprise.sectores.add(s)
        return enterprise

    def update(self, instance, validated_data):
        sectores_data = validated_data.pop('sectores', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if sectores_data is not None:
            instance.sectores.all().delete()
            for sector in sectores_data:
                print(sector)
                if sector.id:
                    instance.sectores.add(Sector.objects.get(pk=sector.id))
                else:
                    s = Sector.objects.create(**sector)
                    instance.sectores.add(s)
        instance.save()
        return instance

    def get_municipio_object(self, object):
        serializer = MunicipioSerializer(instance=object.municipio).data
        return serializer

    def get_provincia_object(self, object):
        return model_to_dict(object.municipio.provincia)

    class Meta:
        model = Enterprise
        fields = '__all__'