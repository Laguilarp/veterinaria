from base.models import Persona
from base.models import Modulo, AccesoModulo
from administrativo.models import PersonaPerfil
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect

def validador(f):
    def funcion1(*args, **kwargs):
        try:
            request = args[0]
            lista_grupos = []
            tiene_acceso = False
            if request.user.is_authenticated:
                persona = Persona.objects.get(id=int(request.session['idpersona']) if 'idpersona' in request.session else request.user.persona.id)
                perfil = PersonaPerfil.objects.filter(status=True, persona=persona)
                if perfil.exists():
                    perfil = perfil.first()
                    if perfil.is_administrador_principal == True:
                        grupo_administrativo_principal = Group.objects.filter(name='Administrativo Principal')
                        if grupo_administrativo_principal:
                            tipoperfil = grupo_administrativo_principal.first().id
                            lista_grupos.append(tipoperfil)
                    if perfil.is_administrador == True:
                        grupo_administrativo = Group.objects.filter(name='Administrativo')
                        if grupo_administrativo:
                            tipoperfil = grupo_administrativo.first().id
                            lista_grupos.append(tipoperfil)
                    if perfil.is_empleado == True:
                        grupo_empleado = Group.objects.filter(name='Empleado')
                        if grupo_empleado:
                            tipoperfil = grupo_empleado.first().id
                            lista_grupos.append(tipoperfil)
                accesos = AccesoModulo.objects.values_list('modulo_id', flat=True).filter(status=True, activo=True,
                                                                                          grupo_id__in=lista_grupos)
                lista_modulos = Modulo.objects.filter(status=True, visible=True, pk__in=accesos)
                for modulo in lista_modulos:
                    if modulo.url_name == request.path:
                        return f(request)
                return HttpResponseRedirect(f"/")


            else:
                HttpResponseRedirect("/")
        except Exception as ex:
            HttpResponseRedirect(f"/?info={ex}")

    return funcion1