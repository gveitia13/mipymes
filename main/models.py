from ckeditor.fields import RichTextField
from django.db import models
from django.utils.safestring import mark_safe
from solo.models import SingletonModel


class Sector(models.Model):
    # enterprise = models.ManyToManyField(Enterprise, related_name='sectores')
    sector = models.CharField('Nombre', max_length=250, unique=True)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    def __str__(self): return self.sector


class Enterprise(models.Model):
    nombre = models.CharField('Nombre', max_length=250, unique=True)
    logo = models.ImageField('Logo', upload_to='enterprise/logo/', null=True, blank=True)
    # provincia = models.CharField('Provincia', max_length=250, )
    municipio = models.ForeignKey('Municipio', max_length=250, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField('Tipo', max_length=250, null=True, blank=True)
    actividad = models.CharField('Actividad', max_length=250)
    representante = models.CharField('Representante', max_length=250, null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=250, null=True, blank=True)
    correo = models.CharField('Correo', max_length=250, null=True, blank=True)
    fecha_aprobacion = models.DateField('Fecha de aprobación', null=True, blank=True)
    is_active = models.BooleanField('Aprobado', default=False)
    sectores = models.ManyToManyField(Sector, related_name='sectores', null=True, blank=True)

    class Meta:
        verbose_name = 'Empresa'
        ordering = ('is_active',)

    def __str__(self):
        return self.nombre

    def get_sectores(self):
        asd = ''
        for i, s in enumerate(self.sectores.all()):
            asd += s.sector
            if i != len(self.sectores.all()) - 1:
                asd += ', '
        return asd

    def get_services(self):
        asd = ''
        for i, s in enumerate(self.servicios.all()):
            asd += s.servicio
            if i != len(self.servicios.all()) - 1:
                asd += ', '
        return asd

    def get_localization(self):
        return f'{self.municipio.provincia} | {self.municipio}'

    get_localization.short_description = 'Localización'
    get_services.short_description = 'Servicios'
    get_sectores.short_description = 'Sectores'


class Service(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='servicios')
    servicio = models.CharField('Servicio', max_length=250)

    class Meta:
        verbose_name = 'Servicio'

    def __str__(self): return self.servicio


class Enlace(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enlaces')
    enlace = models.URLField('Enlace', )
    nombre = models.CharField('Nombre', max_length=250)

    class Meta:
        verbose_name = 'Enlace'

    def __str__(self): return self.enlace


class Publicidad(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='publicidades')
    thumbnail = models.ImageField('Thumbnail', null=True, blank=True, upload_to='publicidad/thumbnail/')
    image = models.ImageField('Imagen', upload_to='publicidad/imagen/')
    link = models.URLField('Link')

    class Meta:
        verbose_name = 'Publicidad'
        verbose_name_plural = 'Publicidades'

    def __str__(self): return self.link


class Contacto(models.Model):
    contact = RichTextField('Contacto')

    def get_contact(self):
        return mark_safe(self.contact)

    get_contact.short_description = 'Contacto'


class Provincia(models.Model):
    nombre = models.CharField('Nombre', max_length=250, unique=True)

    def __str__(self): return self.nombre

    class Meta:
        ordering = ('nombre',)


class Municipio(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='municipios')
    nombre = models.CharField('Nombre', max_length=250, )

    def __str__(self): return self.nombre

    class Meta:
        ordering = ('nombre',)


class PublicidadGeneral(models.Model):
    thumbnail = models.ImageField('Thumbnail', null=True, blank=True, upload_to='publicidad/thumbnail/')
    image = models.ImageField('Imagen', upload_to='publicidad/imagen/')
    link = models.URLField('Link')

    class Meta:
        verbose_name = 'Publicidad general'
        verbose_name_plural = 'Publicidades generales'

    def get_thumbnail(self):
        return mark_safe(f'<img src="{self.thumbnail.url}" height="40"/>') if self.thumbnail else ''

    def get_image(self):
        return mark_safe(f'<img src="{self.image.url}" height="40"/>')

    get_thumbnail.short_description = 'Thumbnail'
    get_image.short_description = 'Imagen'

    def __str__(self): return self.link


class Config(SingletonModel):
    email = models.EmailField('Correo')

    class Meta:
        verbose_name = 'Configuración'

    def __str__(self): return self.email
