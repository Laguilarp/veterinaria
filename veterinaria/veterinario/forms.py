from django import forms
from core.helper_form import FormBase
from baseapp.models import Persona, Genero
from veterinario.models import Raza, SexoMascota, Mascota, Propietario, TipoEspecie, Cita, Veterinario, DetalleCita, \
    Tratamiento, Inyeccion

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = [
                    'especie', 'nombre'
                 ]

        error_messages = {
            'nombre': {
                'unique': "Ya existe raza registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['especie'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'false'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})

        self.fields['especie'].queryset = TipoEspecie.objects.filter(status=True)

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


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
                    'nombres', 'apellido1', 'apellido2', 'tipodocumento', 'documento', 'genero',
                    'fecha_nacimiento', 'direccion', 'correo_electronico', 'telefono'
                 ]

        error_messages = {
            'persona': {
                'unique': "Ya existe persona registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['documento'].max_length = 10
        # Agregar clases CSS específicas a cada campo
        self.fields['nombres'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['apellido1'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})
        self.fields['apellido2'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})
        self.fields['tipodocumento'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['documento'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-4'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['genero'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control date', 'col': 'col-md-6', 'type': 'date', 'format': 'yyyy-mm-dd', 'required':'true'})
        self.fields['correo_electronico'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6'})

        self.fields['genero'].queryset = Genero.objects.filter(status=True)


    def bloquear_campos(self):
        self.fields['nombres'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})
        self.fields['apellido1'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})
        self.fields['apellido2'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})

class AddMascotaForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = [
                    'mascota'
                 ]

        error_messages = {
            'persona': {
                'unique': "Ya existe persona registrada con este nombre."
            }
        }

    def __init__(self, *args, propietario=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['mascota'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['mascota'].queryset = Mascota.objects.filter(status=True)

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
                    'nombre', 'sexo', 'raza', 'color',
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
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'false'})
        self.fields['sexo'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'false'})
        self.fields['raza'].widget.attrs.update({'class': 'form-control', 'data-live-search': 'true', 'col': 'col-md-6', 'required': 'false'})
        self.fields['color'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'false'})
        #self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control date', 'col': 'col-md-6', 'type': 'date', 'format': 'yyyy-mm-dd', 'required':'true'})
        self.fields['peso'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'false'})

        self.fields['nombre'].required = False
        self.fields['sexo'].required = False
        self.fields['raza'].required = False
        self.fields['color'].required = False
        self.fields['peso'].required = False

        self.fields['nombre'].widget.attrs.pop('required', None)
        self.fields['sexo'].widget.attrs.pop('required', None)
        self.fields['raza'].widget.attrs.pop('required', None)
        self.fields['color'].widget.attrs.pop('required', None)
        self.fields['peso'].widget.attrs.pop('required', None)

        self.fields['raza'].queryset = Raza.objects.filter(status=True)
        self.fields['sexo'].queryset = SexoMascota.objects.filter(status=True)

class MascotaPropietarioForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
                    'nombre', 'sexo', 'raza', 'color',
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
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'id': 'nombre', 'required': 'true'})
        self.fields['sexo'].widget.attrs.update({'class': 'form-control', 'id': 'sexo', 'data-live-search': 'true', 'required': 'true'})
        self.fields['raza'].widget.attrs.update({'class': 'form-control', 'id': 'raza', 'data-live-search': 'true', 'required': 'true'})
        self.fields['color'].widget.attrs.update({'class': 'form-control', 'id': 'color', 'required': 'true'})
        #self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control date', 'id': 'fecha_nacimiento', 'type': 'date', 'required': 'true'})
        self.fields['peso'].widget.attrs.update({'class': 'form-control', 'id': 'peso', 'required': 'true'})

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

class DetalleCitaForm(forms.ModelForm):
    class Meta:
        model = DetalleCita
        fields = [
                    'tratamiento', 'inyeccion', 'observacion'
                 ]

        error_messages = {

        }

    def __init__(self, *args, propietario=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS específicas a cada campo
        self.fields['tratamiento'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['inyeccion'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['observacion'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        #self.fields['precio_total'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['tratamiento'].queryset = Tratamiento.objects.filter(status=True)
        self.fields['inyeccion'].queryset = Inyeccion.objects.filter(status=True)
