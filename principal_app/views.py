from django.shortcuts import render
from principal_app import models
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
import  os
import shutil
# Create your views here.

usuariosActivos =[]

def serveHome(request):
    return render(request,'home.html')

def serveRegistro(request):
    return render(request,'registro.html')

def crearRegistro(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('user') and request.POST.get('pass') and request.POST.get('cPass'):
            if request.POST.get('pass') == request.POST.get('cPass'):
                try:
                    usuario = models.Usuario(nombre_usuario = request.POST.get('user'), nombre = request.POST.get('nombre'), apellidos = request.POST.get('apellido'), correo_electronico = request.POST.get('email'), contrasena = request.POST.get('pass'))
                    usuario.save()

                    os.mkdir("./media/"+usuario.nombre_usuario)

                    return render(request, 'login.html')
                except:
                    messages.error(request, 'Nombre de usuario o correo ya estan en uso')
                    return render(request, 'registro.html')
            else:

                messages.error(request, 'Las contrasenas no coinciden')
                return render(request, 'registro.html')

        else:
            messages.error(request, 'Por favor diligencie todos los espacios')
            return render(request, 'registro.html')

def login(request):
    return render(request, 'login.html')

def auteticarIngreso(request):
    print(request)
    if request.method == 'POST':
        if request.POST.get('usuario') and request.POST.get('contrasena'):
            u = request.POST.get('usuario')
            c = request.POST.get('contrasena')
            usuario = models.Usuario.objects.filter(nombre_usuario = u, contrasena = c)
            if usuario:
                usuario=usuario[0]
                if usuario not in usuariosActivos: usuariosActivos.append(usuario)
                proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
                print(len(usuariosActivos))

                return render(request,'bancoProyectos.html',{'proyectos' :proyectos})
            else:
                messages.error(request, 'Usuario o contraseña incorrecto')
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'home.html')

def serveBancoProyectos(request):
    nom = request.POST.get("usrname")
    usuario = models.Usuario.objects.filter(nombre_usuario=nom)[0]
    proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
    return render(request, 'bancoProyectos.html', {'proyectos': proyectos})

def crearProyecto(request):
    if request.POST.get("usrname") and request.POST.get("name"):
        try:
            nom=request.POST.get("usrname")
            usuario = models.Usuario.objects.filter(nombre_usuario=nom)[0]

            if usuario in usuariosActivos:
                proyname=request.POST.get("name")
                proy = models.Proyecto.objects.filter(nombre=proyname)
                if proy.__len__() ==0 :
                    proyecto =models.Proyecto(usuario=usuario,nombre=proyname)
                    proyecto.save()
                    os.mkdir("./media/"+usuario.nombre_usuario+"/"+proyname)
                else:
                    messages.error(request, "el nombre del proyecto debe ser diferente a los demas")
                proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
                return render(request, 'bancoProyectos.html', {'proyectos': proyectos})
            else:
                return render(request,'home.html')
        except:
            print()
    proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
    return render(request,'bancoProyectos.html',{'proyectos' : proyectos})

def serveBancoTrabajo(request):
    try:
        return render(request,'index.html')
    except Exception as e:
        print(e)
    return HttpResponse("ok")

def serveArchivo(request):
    response = HttpResponse(open(os.path.join("./media/firstProject/", "guitar.mp3"), "rb").read(),content_type="audio/mp3")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format("guitar.mp3")
    return response

def serveManifest(request):
    return  HttpResponse(open("./principal_app/static/asset-manifest.json").read())

def borrarProyecto(request):
    if request.POST.get("usr") and request.POST.get("nom"):
        try:
            nom = request.POST.get("usr")
            usuario = models.Usuario.objects.filter(nombre_usuario=nom)[0]
            print(nom)
            if usuario in usuariosActivos:
                proyname = request.POST.get("nom")
                proy = models.Proyecto.objects.filter(usuario=usuario.id_usuario, nombre=proyname)
                if proy.__len__() == 1:
                    proy = proy[0]
                    proy.delete()
                    os.rmdir("./media/"+usuario.nombre_usuario+"/"+proyname)
                else:
                    messages.error(request, "El proyecto no existe")
                proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
                return render(request, 'bancoProyectos.html', {'proyectos': proyectos})
            else:
                return render(request, 'home.html')
        except:
            print()
        proyectos = models.Proyecto.objects.filter(usuario=usuario.id_usuario)
        return render(request, 'bancoProyectos.html', {'proyectos': proyectos})
    else:
        return render(request, 'home.html')
