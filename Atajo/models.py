from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
#from django.contrib.gis.db import models
# Create your models here.


TIPO_IMAGEN = [
    ('GRA', 'GRANO'),
    ('ELA', 'ELABORADO'),
    ('PLA', 'PLANTA'),
]

UNIDAD_MEDIDA = [
    ('Lb','Libra'),
    ('Kg','Kilogramo'),
    ('g','Gramo'),
    ('U','Unidad'),
    ('Lt','Lata'),
    ('Gc','Guacál'),
]

ESTADO = [
    ('B','BUENO'),
    ('R','REGULAR'),
    ('M','MALO'),
]

class Transporte(models.Model):
    chapa = models.CharField(max_length=15)
    modelo = models.CharField(max_length=15)
    marca = models.CharField(max_length=15)

    def __str__(self):
        return '%s' % self.chapa + " - " + '%s' % self.marca + " - " + '%s' % self.modelo

    class Meta:
        ordering = ['chapa']


class Ruta(models.Model):
    fecha_hora = models.DateTimeField()
    itinerario = JSONField()  # todo: comprobar
    transporte = models.ForeignKey('Transporte', on_delete=models.SET_NULL, related_name='Ruta', null=True)

    def __str__(self):
        return '%s' % self.fecha_hora

    class Meta:
        ordering = ['fecha_hora']


class Obrero(models.Model):
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=40)
    num_ci = models.PositiveIntegerField()
    correo = models.EmailField()
    movil = models.PositiveIntegerField()
    parcela = models.ForeignKey('Parcela', on_delete=models.SET_NULL, related_name='Obrero', null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre + " - " + '%s' % self.apellidos + " - " + '%s' % self.num_ci

    class Meta:
        ordering = ['nombre']


class Parcela(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    pais = models.CharField(max_length=20, null=True, blank=True)
    provincia = models.CharField(max_length=30, null=True, blank=True)
    municipio = models.CharField(max_length=30, null=True, blank=True)
    consejo_popular = models.CharField(max_length=30, null=True, blank=True)
    longitud = models.CharField(max_length=20)  # PointField()
    latitud = models.CharField(max_length=20)
    ancho = models.FloatField()
    largo = models.FloatField()
    pos_id = models.IntegerField()
    agricultor = models.ForeignKey('Agricultor', on_delete=models.SET_NULL, related_name='Parcela', null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre + " - " + '%s' % self.direccion

    class Meta:
        ordering = ['nombre']


class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.FloatField()
    unidad_medida = models.CharField(max_length=2, choices=UNIDAD_MEDIDA, default='Lb')
    estado = models.CharField(max_length=1, choices=ESTADO, default='B')
    fecha_cosecha = models.DateField()
    codigo = models.CharField(max_length=10)
    precio = models.FloatField()
    parcela = models.ForeignKey('Parcela', on_delete=models.SET_NULL, related_name='Cultivo', null=True)
    orden_entrega = models.ForeignKey('OrdenEntrega', on_delete=models.SET_NULL, related_name='Cultivo', null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre + " - " + '%s' % self.codigo + " - " + '%s' % self.cantidad

    class Meta:
        ordering = ['nombre']


class Agricultor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=40)
    apodo = models.CharField(max_length=10)
    num_ci = models.PositiveIntegerField()
    direccion = models.CharField(max_length=100)
    pais = models.CharField(max_length=20)
    provincia = models.CharField(max_length=30)
    municipio = models.CharField(max_length=30)
    consejo_popular = models.CharField(max_length=30, null=True, blank=True)
    correo = models.EmailField()
    telefono = models.PositiveIntegerField()
    longitud = models.CharField(max_length=20)  # PointField()
    latitud = models.CharField(max_length=20)
    pos_id = models.IntegerField()

    def __str__(self):
        return '%s' % self.direccion + " - " + '%s' % self.nombre + " " + '%s' % self.apellidos

    class Meta:
        ordering = ['direccion']
    

class PaqueteSemillas(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio = models.FloatField()
    d_plantas = models.PositiveIntegerField()
    d_hileras = models.PositiveIntegerField()
    d_profundidad = models.FloatField()
    t_germinacion = models.PositiveIntegerField()
    t_trasplante = models.PositiveIntegerField()
    t_cosecha = models.PositiveIntegerField()
    p_biocida = models.PositiveIntegerField()
    p_fungicida = models.PositiveIntegerField()
    p_fertilizante = models.PositiveIntegerField()
    agricultor = models.ForeignKey('Agricultor', on_delete=models.CASCADE, related_name='PaqueteSemillas', null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre + " - " + '%s' % self.cantidad + " " + '%s' % self.precio

    class Meta:
        ordering = ['nombre']


class Celda(models.Model):
    longitud = models.FloatField()
    latitud = models.FloatField()
    f_siembra = models.DateField()
    f_germinacion = models.DateField()
    f_trasplante = models.DateField()
    f_cosecha = models.DateField()
    paquete_semillas = models.ForeignKey('PaqueteSemillas', on_delete=models.SET_NULL, related_name='Celda', null=True)
    parcela = models.ForeignKey('Parcela', on_delete=models.CASCADE, related_name='Celda')

    def __str__(self):
        return '%s' % self.longitud + " - " + '%s' % self.latitud

    class Meta:
        ordering = ['f_cosecha']


class Imagen(models.Model):
    nombre = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPO_IMAGEN, default='GRA')
    paquete_semillas = models.ForeignKey('PaqueteSemillas', on_delete=models.SET_NULL, related_name='imagen', null=True)
    cultivo = models.ForeignKey('Cultivo', on_delete=models.SET_NULL, related_name='imagen', null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre + " - " + '%s' % self.direccion

    class Meta:
        ordering = ['nombre']


class OrdenEntrega(models.Model):
    codigo = models.CharField(max_length=10)
    fecha_hora = models.DateTimeField()
    ruta_asig = models.IntegerField(blank=True, null=True)
    agricultor = models.ForeignKey('Agricultor', on_delete=models.SET_NULL, related_name='OrdenEntrega', null=True)
    transporte = models.ForeignKey('Transporte', on_delete=models.SET_NULL, related_name='OrdenEntrega', null=True, blank=True)
    parcela = models.ForeignKey('Parcela', on_delete=models.SET_NULL, related_name='OrdenEntrega', null=True)

    def __str__(self):
        return '%s' % self.codigo + " - " + '%s' % self.fecha_hora

    class Meta:
        ordering = ['codigo']