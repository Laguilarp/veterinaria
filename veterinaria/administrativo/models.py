from django.db import models
from base.helper_model import ModeloBase
from base.models import Persona, Genero

# Create your models here.
class PersonaPerfil(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    is_administrador_principal = models.BooleanField(default=False, verbose_name=u'Es administrador principal?')
    is_administrador = models.BooleanField(default=False, verbose_name=u'Es administrador?')
    is_empleado = models.BooleanField(default=False, verbose_name=u'Es empleado?')

    class Meta:
        verbose_name = "Perfil de personas"
        verbose_name_plural = "Perfiles de personas"
        ordering = ['id']

    def nombre_persona(self):
        return self.persona.__str__()

    def __str__(self):
        if self.es_administrador() and self.es_empleado():
            return u'%s - %s' % (self.nombre_persona(), "ADMINISTRADOR - EMPLEADO")
        elif not self.es_administrador() and self.es_empleado():
            return u'%s - %s' % (self.nombre_persona(), "EMPLEADO")
        elif self.es_administrador() and not self.es_empleado():
            return u'%s - %s' % (self.nombre_persona(), "ADMINISTRADOR")
        else:
            return u'%s' % "NO TIENE PERFIL"

    def es_empleado(self):
        return self.is_empleado

    def es_administrador(self):
        return self.is_administrador