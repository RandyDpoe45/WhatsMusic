from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=30, unique= True)
    nombre = models.CharField(max_length=50)
    apellidos= models.CharField(max_length=50)
    correo_electronico= models.CharField(max_length=60, unique= True)
    contrasena=models.CharField(max_length=128)

class Proyecto(models.Model):
    id_proyecto= models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre= models.CharField(max_length=30)


class Pista(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ruta = models.CharField(max_length=300)