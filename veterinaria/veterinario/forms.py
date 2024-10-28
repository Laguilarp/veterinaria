from django import forms
from core.helper_form import FormBase
from baseapp.models import Persona, Genero
from veterinario.models import Raza, SexoMascota, Mascota, Propietario, TipoEspecie, Cita, Veterinario

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

class EspecieForm(forms.ModelForm):
    class Meta:
        model = TipoEspecie
        fields = [
                    'nombre'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe especie registrada con este nombre."
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

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
                    'mascota', 'veterinario', 'fecha_cita', 'hora_cita', 'motivo'
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['mascota'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['veterinario'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'true'})
        self.fields['fecha_cita'].widget.attrs.update({'class': 'form-control date', 'col': 'col-md-6', 'type': 'datetime-local', 'format': 'yyyy-mm-ddTHH:MM', 'required':'true'})
        self.fields['hora_cita'].widget = forms.TimeInput(attrs={'class': 'form-control', 'col': 'col-md-6','type': 'time','required': 'true'},format='%H:%M')
        self.fields['hora_cita'].input_formats = ['%H:%M']
        self.fields['motivo'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})

        self.fields['mascota'].queryset = Mascota.objects.filter(status=True)
        self.fields['veterinario'].queryset = Veterinario.objects.filter(status=True)