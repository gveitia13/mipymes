from django.contrib import admin

from main.models import *


class ServiceInline(admin.TabularInline):
    model = Service
    # exclude = ['enterprise']
    extra = 3


class EnlaceInline(admin.TabularInline):
    model = Enlace
    extra = 3
    # exclude = ['enterprise']


class SectorInline(admin.TabularInline):
    model = Sector
    extra = 3
    # exclude = ['enterprise']


class PublicidadInline(admin.StackedInline):
    # exclude = ['enterprise']
    model = Publicidad
    extra = 3


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('get_contact',)


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_localization', 'correo', 'actividad', 'get_sectores', 'is_active')
    list_editable = ('is_active',)
    list_per_page = 15
    search_fields = ('nombre',)
    list_filter = ('is_active', 'municipio')
    inlines = [PublicidadInline, ServiceInline, EnlaceInline]
    filter_horizontal = ['sectores', ]
    fieldsets = [
        ('General', {"fields": (
            "nombre", "logo", 'municipio', 'tipo', 'actividad', 'representante', 'telefono', 'correo',
            'fecha_aprobacion', 'is_active')}),
        ('Sectores', {"fields": ("sectores",)}),
    ]
    change_list_template = 'admin/enterprise_change_list.html'


class SectorAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ('sector',)
    change_list_template = 'admin/sector_change_list.html'


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    change_list_template = 'admin/provincia_change_list.html'


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_per_page = 20
    list_display = ('nombre', 'provincia')
    ordering = ('provincia',)
    list_filter = ('provincia',)


admin.site.register(Sector, SectorAdmin)
