from django import forms
from administrativo.models import Cargo, DatosOrganizacion, Genero
from core.core import DIAS_SEMANA, PARENTESCOS
class DatosOrganizacionForm(forms.ModelForm):
    class Meta:
        model = DatosOrganizacion
        fields = [
                    'nombre', 'direccion', 'latitud', 'longitud', 'radio'
                 ]

        error_messages = {
            'persona': {
                'unique': "Ya existe detalle en la jornada laboral registrado con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'true', 'type': 'text', 'placeholder': 'Nombre'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'true', 'type': 'text', 'placeholder': 'Dirección'})
        self.fields['latitud'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required': 'true', 'type': 'input', 'placeholder': 'Latitud'})
        self.fields['longitud'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required': 'true', 'type': 'input', 'placeholder': 'Longitud'})
        self.fields['radio'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required': 'true', 'type': 'input', 'placeholder': 'Radio'})

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = [
                    'nombre'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe cargo registrado con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-18', 'style': 'width:700px'})