from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from .models import Usuario
from .forms import UserForm

def conseguir_crear_grupo(grupo, perm_strings):
    group, created = Group.objects.get_or_create(name=grupo) # consigueme un grupo que exista con este nombre. Si no existe, crealo, y dime con un booleano si justo se creo

    if created:
        for perm_string in perm_strings:
            app_label, codename = perm_string.split('.')
            perm = Permission.objects.get(
                content_type__app_label = app_label,
                codename = codename
            )
            group.permissions.add(perm)

    return group

def registrar(req, staff, grupo, grupo_perms, ruta_html):
    if req.method == 'POST':
        form = UserForm(req.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return redirect(reverse('registrar') + '?pass')

            if User.objects.filter(username = username).exists():
                return redirect(reverse('registrar') + '?fail')

            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            direccion = form.cleaned_data['direccion']

            user = User.objects.create_user(username = username, password = password)
            usuario = Usuario.objects.create(username = username, cuenta = user, nombre = nombre, apellidos = apellidos, direccion = direccion)

            user.is_staff = staff
            user.save()
            usuario.save()

            group = conseguir_crear_grupo(grupo, grupo_perms)
            user.groups.add(group)

            return redirect('home')

    else:
        form = UserForm()

    return render(req, ruta_html, { 'form': form })

def registrar_usuario(req):
    grupo_perms = {
        "catalogo.view_obra, checkout.add_boletadecompra, catalogo.view_publicacion, catalogo.view_etiqueta"
    }
    return registrar(req, False, "Usuarios", grupo_perms, 'usuarios/registrar.html')

def registrar_admin(req):
    grupo_perms = {
        "catalogo.view_publicacion, catalogo.delete_obra, catalogo.view_etiqueta, usuarios.view_usuario, contenttypes.view_contenttype, usuarios.add_usuario, catalogo.add_publicacion, contenttypes.delete_contenttype, checkout.delete_boletadecompra, usuarios.delete_usuario, catalogo.delete_etiqueta, auth.view_user, catalogo.change_publicacion, checkout.change_boletadecompra, auth.delete_user, catalogo.change_etiqueta, auth.view_permission, catalogo.delete_publicacion, catalogo.change_obra, contenttypes.change_contenttype, catalogo.add_etiqueta, auth.view_group, auth.add_user, usuarios.change_usuario, checkout.view_boletadecompra, auth.change_user, sessions.view_session, catalogo.view_obra, admin.view_logentry, contenttypes.add_contenttype, catalogo.add_obra"
    }
    return registrar(req, True, "Administradores", grupo_perms, 'usuarios/registrar_admin.html')

@login_required
def perfil(req):
    usuario = Usuario.objects.get(cuenta__id = req.user.id)
    return render(req, "usuarios/perfil.html", {"usuario": usuario})

@login_required
def eliminar_usuario(req):
    cuenta = User.objects.get(id = req.user.id)
    usuario = Usuario.objects.get(cuenta__id = cuenta.id)
    if req.method == "POST":
        usuario.delete()
        cuenta.delete()
        return redirect(reverse('home'))
    return render(req, "usuarios/eliminar_usuario.html", {"usuario": usuario})