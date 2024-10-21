from django import forms
from core.helper_form import FormBase
from baseapp.models import Persona, Genero
from veterinario.models import Raza, SexoMascota, Mascota, Propietario, TipoEspecie

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = [
                    'nombre'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe raza registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})

class SexoMascotaForm(forms.ModelForm):
    class Meta:
        model = SexoMascota
        fields = [
                    'nombre'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe sexo registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
                    'propietario', 'nombre', 'especie', 'sexo', 'raza', 'color', 'fecha_nacimiento',
                    'peso'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe mascota registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['propietario'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['especie'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['sexo'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['raza'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['color'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control date', 'col': 'col-md-6', 'type': 'date', 'format': 'yyyy-mm-dd', 'required':'true'})
        self.fields['peso'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})

        self.fields['propietario'].queryset = Propietario.objects.filter(status=True)
        self.fields['especie'].queryset = TipoEspecie.objects.filter(status=True)
        self.fields['raza'].queryset = Raza.objects.filter(status=True)
        self.fields['sexo'].queryset = SexoMascota.objects.filter(status=True)