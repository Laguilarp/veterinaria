from django.db import models
from core.helper_model import ModeloBase
from core.core import IDENTIFICACIONES
from baseapp.models import Persona, Genero
from core.core import DIAS_SEMANA, PARENTESCOS

class DatosOrganizacion(ModeloBase):
    nombre = models.CharField(blank=True, null=True, max_length=500, verbose_name=u"Nombre de la empresa")
    direccion = models.CharField(blank=True, null=True, max_length=500, verbose_name=u"Dirección de la empresa")
    latitud = models.FloatField(default=0, blank=True, null=True, verbose_name="Latitud")
    longitud = models.FloatField(default=0, blank=True, null=True, verbose_name="Longitud")
    radio = models.FloatField(default=0, blank=True, null=True, verbose_name="Radio disponible para marcar")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['id']

    def __str__(self):
        return f"{self.nombre}"

class PersonaPerfil(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    is_administrador = models.BooleanField(default=False, verbose_name=u'Es administrador?')
    is_veterinario = models.BooleanField(default=False, verbose_name=u'Es veterinario?')

    class Meta:
        verbose_name = "Perfil de persona"
        verbose_name_plural = "Perfiles de personas"
        ordering = ['id']

    def nombre_persona(self):
        return self.persona.__str__()

    def __str__(self):
        if self.es_administrador() and self.es_veterinario():
            return u'%s - %s' % (self.nombre_persona(), "ADMINISTRADOR - VETERINARIO")
        elif not self.es_administrador() and self.es_veterinario():
            return u'%s - %s' % (self.nombre_persona(), "VETERINARIO")
        elif self.es_administrador() and not self.es_veterinario():
            return u'%s - %s' % (self.nombre_persona(), "ADMINISTRADOR")
        else:
            return u'%s' % "NO TIENE PERFIL"

    def es_veterinario(self):
        return self.is_veterinario

    def es_administrador(self):
        return self.is_administrador

class Cargo(ModeloBase):
    nombre = models.CharField(blank=True, null=True, max_length=300, verbose_name=u"Nombre del cargo")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().capitalize()
        super(Cargo, self).save(*args, **kwargs)