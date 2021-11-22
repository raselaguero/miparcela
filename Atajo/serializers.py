from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Parcela, Transporte, Obrero, Agricultor, OrdenEntrega, Cultivo, Ruta, PaqueteSemillas, Imagen, Celda


class ImagenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Imagen
        fields = ['id', 'nombre', 'direccion', 'tipo', 'paquete_semillas', 'cultivo']
        read_only_fields = ('id',)
        extra_kwargs = {'cultivo': {'required': False}, 'paquete_semillas': {'required': True}}


class CultivoSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Cultivo
        fields = ['id', 'nombre', 'codigo', 'precio', 'cantidad', 'unidad_medida', 'estado', 'fecha_cosecha', 'parcela',
                  'orden_entrega']
        read_only_fields = ('id',)
        extra_kwargs = {'orden_entrega': {'required': False}}


class OrdenEntregaSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = OrdenEntrega
        fields = ['id', 'codigo', 'fecha_hora', 'ruta_asig', 'agricultor', 'transporte', 'parcela']
        read_only_fields = ('id',)
        extra_kwargs = {'trasporte': {'required': False}, 'ruta_asig': {'required': False}}


class UserSerializer(serializers.ModelSerializer): # todo: OK

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_active', 'is_staff', 'last_login', 'date_joined']
        read_only_fields = ('id', 'last_login', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}


class ObreroSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Obrero
        fields = ['id', 'nombre', 'apellidos', 'num_ci', 'correo', 'movil', 'parcela']
        read_only_fields = ('id',)


class CeldaSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Celda
        fields = ['id', 'longitud', 'latitud', 'f_siembra', 'f_germinacion', 'f_trasplante', 'f_cosecha',
                  'paquete_semillas', 'parcela']
        read_only_fields = ('id',)
        extra_kwargs = {'parcela': {'required': True}, 'paquete_semillas': {'required': True}}


class ParcelaSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Parcela
        fields = ['id', 'nombre', 'direccion', 'pais', 'provincia', 'municipio', 'consejo_popular', 'ancho', 'largo',
                  'longitud', 'latitud', 'pos_id', 'agricultor']
        read_only_fields = ('id',)
        extra_kwargs = {'agricultor': {'required': False}}


class PaqueteSemillasSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = PaqueteSemillas
        fields = ['id', 'nombre', 'descripcion', 'cantidad', 'precio', 'd_plantas', 'd_hileras', 'd_profundidad',
                  't_germinacion', 't_trasplante', 't_cosecha', 'p_biocida', 'p_fungicida', 'p_fertilizante',
                  'agricultor']
        read_only_fields = ('id',)
        extra_kwargs = {'agricultor': {'required': False}}


class AgricultorSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Agricultor
        fields = ['id', 'nombre', 'apellidos', 'apodo', 'num_ci', 'direccion', 'pais', 'provincia', 'municipio',
                  'consejo_popular', 'correo', 'telefono', 'longitud', 'latitud', 'pos_id', 'user']
        read_only_fields = ('id',)
        extra_kwargs = {'user': {'required': True}}


class RutaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruta
        fields = ['fecha_hora', 'itinerario']
        read_only_fields = ('id',)


class TransporteSerializer(serializers.ModelSerializer):  # todo: OK

    class Meta:
        model = Transporte
        fields = ['id', 'chapa', 'modelo', 'marca']
        read_only_fields = ('id',)

