from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import filters

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from Atajo.models import Cultivo, Obrero, Parcela, OrdenEntrega, Agricultor, Transporte, Ruta, PaqueteSemillas, Imagen
from Atajo.serializers import ObreroSerializer, CultivoSerializer, ParcelaSerializer, OrdenEntregaSerializer, \
    AgricultorSerializer, TransporteSerializer, PaqueteSemillasSerializer, ImagenSerializer, UserSerializer

import requests
import os

os.environ['no_proxy'] = '127.0.0.1,localhost'


# Create your views here.
class RegisterView(APIView):

    def get(self, request, format=None):
        return Response({'detail': "GET Response"})

    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response('Invalid JSON - {0}'.format(error.detail), status=status.HTTP_400_BAD_REQUEST)
        if "username" not in data and "password" not in data:
            return Response('Wrong credentials', status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = authenticate(username=data['username'], password=data['password'])
            if not user:
                user = User.objects.create_user(username=data['username'], password=data['password'])
            token = Token.objects.get_or_create(user=user)
            header = "http://localhost:8888/Osm2poService?cmd=fv&lon="
            footer = "&format=geojson"
            response = requests.get(header + data['longitud'] + "&lat=" + data['latitud'] + footer).json()
            print(response['properties']['id'])
            Agricultor.objects.create(nombre=data['nombre'], apellidos=data['apellidos'], num_ci=data['num_ci'],
                                      direccion=data['direccion'], pais=data['pais'], provincia=data['provincia'],
                                      municipio=data['municipio'], consejo_popular=request.data['consejo_popular'],
                                      correo=data['correo'], telefono=data['telefono'], longitud=data['longitud'],
                                      latitud=data['latitud'], pos_id=response['properties']['id'], user=user)
        return Response({'detail': 'POST answer', 'token': token[0].key})


class UserMixin(object):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()

    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('username',)
    ordering = ['username']


class UserLista(UserMixin, ListCreateAPIView):
    pass


class UserDetalle(UserMixin, RetrieveUpdateDestroyAPIView):
    pass


class AgricultorMixin(object):  # TODO: EN IMPLEMENTACIÓN
    #permission_classes = (IsAuthenticated,)
    queryset = Agricultor.objects.all()
    serializer_class = AgricultorSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre', 'num_ci', 'telefono')
    ordering_fields = ('nombre', 'num_ci')
    ordering = ['nombre']


class AgricultorLista(AgricultorMixin, ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        header = "http://localhost:8888/Osm2poService?cmd=fv&lon="
        footer = "&format=geojson"
        response = requests.get(header + request.data['longitud'] + "&lat=" + request.data['latitud'] + footer).json()
        #print(response['properties']['id'])
        data = {'nombre': request.data['nombre'], 'apellidos': request.data['apellidos'],
                'apodo': request.data['apodo'], 'num_ci': request.data['num_ci'],
                'direccion': request.data['direccion'], 'pais': request.data['pais'],
                'provincia': request.data['provincia'], 'municipio': request.data['municipio'],
                'consejo_popular': request.data['consejo_popular'], 'correo': request.data['correo'],
                'telefono': request.data['telefono'], 'longitud': request.data['longitud'],
                'latitud': request.data['latitud'], 'pos_id': response['properties']['id'], 'user': request.data['user']}
        serializer = AgricultorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgricultorDetalle(AgricultorMixin, RetrieveUpdateDestroyAPIView):  # TODO: EN IMPLEMENTACIÓN
    def put(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['user'])
        orden_entrega = Parcela.objects.get(pk=request.data['orden_entrega'])
        paquete_semillas = PaqueteSemillas.objects.get(pk=request.data['paquete_semillas'])
        parcela = Parcela.objects.get(pk=request.data['parcela'])
        agricultor_instance = Agricultor.objects.get(pk=request.data['id'])
        header = "http://localhost:8888/Osm2poService?cmd=fv&lon="
        footer = "&format=geojson"
        response = requests.get(header + request.data['longitud'] + "&lat=" + request.data['latitud'] + footer).json()
        print(response['properties']['id'])
        agricultor = Agricultor.objects.filter(pk=request.data['id']).update(nombre=request.data['nombre'],
                                                                             apellidos=request.data['apellidos'],
                                                                             apodo=request.data['apodo'],
                                                                             num_ci=request.data['num_ci'],
                                                                             direccion=request.data['direccion'],
                                                                             pais=request.data['pais'],
                                                                             provincia=request.data['provincia'],
                                                                             municipio=request.data['municipio'],
                                                                             consejo_popular=request.data['consejo_popular'],
                                                                             correo=request.data['correo'],
                                                                             telefono=request.data['telefono'],
                                                                             longitud=request.data['longitud'],
                                                                             latitud=request.data['latitud'],
                                                                             pos_id=response['properties']['id'],
                                                                             user=user, orden_entrega=orden_entrega,
                                                                             paquete_semillas=paquete_semillas,
                                                                             parcela=parcela)
        serializer = AgricultorSerializer(agricultor_instance, data=agricultor)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParcelaMixin(object):
    #permission_classes = (IsAdminUser,)
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre',)
    ordering_fields = ('nombre', 'provincia')
    ordering = ['nombre']


class ParcelaLista(ParcelaMixin, ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        header = "http://localhost:8888/Osm2poService?cmd=fv&lon="
        footer = "&format=geojson"
        response = requests.get(header + request.data['longitud'] + "&lat=" + request.data['latitud'] + footer).json()
        #print(response['properties']['id'])
        data = {'nombre': request.data['nombre'], 'direccion': request.data['direccion'], 'pais': request.data['pais'],
                'provincia': request.data['provincia'], 'municipio': request.data['municipio'],
                'consejo_popular': request.data['consejo_popular'], 'longitud': request.data['longitud'],
                'latitud': request.data['latitud'], 'ancho': request.data['ancho'], 'largo': request.data['largo'],
                'pos_id': response['properties']['id'], 'agricultor': request.data['agricultor']}
        serializer = ParcelaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParcelaDetalle(ParcelaMixin, RetrieveUpdateDestroyAPIView):  # TODO: EN IMPLEMENTACIÓN
    def put(self, request, *args, **kwargs):
        parcela_instance = Parcela.objects.get(pk=request.data['id'])
        header = "http://localhost:8888/Osm2poService?cmd=fv&lon="
        footer = "&format=geojson"
        response = requests.get(header + request.data['longitud'] + "&lat=" + request.data['latitud'] + footer).json()
        print(response['properties']['id'])
        parcela = Parcela.objects.filter(pk=request.data['id']).update(nombre=request.data['nombre'],
                                                                       direccion=request.data['direccion'],
                                                                       pais=request.data['pais'],
                                                                       provincia=request.data['provincia'],
                                                                       municipio=request.data['municipio'],
                                                                       consejo_popular=request.data['consejo_popular'],
                                                                       longitud=request.data['longitud'],
                                                                       latitud=request.data['latitud'],
                                                                       ancho=request.data['ancho'],
                                                                       largo=request.data['largo'],
                                                                       pos_id=response['properties']['id'],
                                                                       agricultor=request.data['agricultor'])
        serializer = ParcelaSerializer(parcela_instance, data=parcela)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaqueteSemillasMixin(object):
    permission_classes = (IsAdminUser,)
    queryset = PaqueteSemillas.objects.all()
    serializer_class = PaqueteSemillasSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre',)
    ordering_fields = ('nombre', 'precio')
    ordering = ['nombre']


class PaqueteSemillasLista(PaqueteSemillasMixin, ListCreateAPIView):
    pass


class PaqueteSemillasDetalle(PaqueteSemillasMixin, RetrieveUpdateDestroyAPIView):
    pass


class ObreroMixin(object):
    permission_classes = (IsAdminUser,)
    queryset = Obrero.objects.all()
    serializer_class = ObreroSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre', 'num_ci', 'movil')
    ordering_fields = ('nombre', 'num_ci', 'movil')
    ordering = ['nombre']


class ObreroLista(ObreroMixin, ListCreateAPIView):
    pass


class ObreroDetalle(ObreroMixin, RetrieveUpdateDestroyAPIView):
    pass


class ImagenMixin(object):
    permission_classes = (IsAdminUser,)
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre', 'tipo')
    ordering_fields = ('nombre', 'tipo')
    ordering = ['nombre']


class ImagenLista(ImagenMixin, ListCreateAPIView):
    pass


class ImagenDetalle(ImagenMixin, RetrieveUpdateDestroyAPIView):
    pass


class TransporteMixin(object):
    permission_classes = (IsAdminUser,)
    queryset = Transporte.objects.all()
    serializer_class = TransporteSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('chapa', 'marca')
    ordering_fields = ('chapa',)
    ordering = ['chapa']


class TransporteLista(TransporteMixin, ListCreateAPIView):
    pass


class TransporteDetalle(TransporteMixin, RetrieveUpdateDestroyAPIView):
    pass


class CultivoMixin(object):
    queryset = Cultivo.objects.all()
    serializer_class = CultivoSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('nombre', 'codigo', 'precio')
    ordering_fields = ('nombre', 'codigo', 'precio')
    ordering = ['nombre']


class CultivoLista(CultivoMixin, ListAPIView):
    permission_classes = (IsAuthenticated,)


class CultivoCrear(CultivoMixin, CreateAPIView):
    permission_classes = (IsAdminUser,)


class CultivoDetalle(CultivoMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)


class OrdenEntregaMixin(object):
    queryset = OrdenEntrega.objects.all()
    serializer_class = OrdenEntregaSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('codigo', 'fecha_hora')
    ordering_fields = ('codigo', 'fecha_hora', 'ruta_asig')
    ordering = ['codigo']


class OrdenEntregaLista(OrdenEntregaMixin, ListCreateAPIView):
    permission_classes = (IsAuthenticated,)


class OrdenEntregaDetalle(OrdenEntregaMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)


class Ubicacion(APIView):  # TODO: en implementación
    def post(self, request, *args, **kwargs):
        data = request.data
        lista = []
        transp = Transporte.objects.get(pk=data['id'])
        orden = OrdenEntrega.objects.filter(transporte__chapa=transp.chapa, fecha_hora__lte=data['fecha_hora'],
                                            ruta_asig=None)
        lista.append(str(transp.base.pos_id))
        lista.extend([str(i.cliente.pos_id) for i in orden])
        lista.append(str(transp.base.pos_id))
        fh_ruta = data['fecha_hora']
        pk_transp = data['id']
        ruta(lista, fh_ruta, pk_transp)


def ruta(var, fh_ruta, pk_transp):  # TODO: en implementación
    header = "http://localhost:8888/Osm2poService?cmd=ft&tsp="
    footer = "&findShortestPath=true&maxCost=20.0&format=geojson"
    cnv = ','.join(var)
    response = requests.get(header + cnv + footer)
    r = response.json()
    transp = Transporte.objects.get(pk=pk_transp)
    ruta = Ruta.objects.create(fecha_hora=fh_ruta, transporte=transp, itinerario=r)
    orden = OrdenEntrega.objects.filter(transporte__chapa=transp.chapa, fecha_hora__lte=fh_ruta, ruta_asig=None)
    for item in orden:
        item.ruta_asig = ruta.id
        item.save()


class Trazo(APIView):  # TODO: en implementación
    def post(self, request, *args, **kwargs):
        data = request.data
        ruta = Ruta.objects.get(id=data['id'])
        itinerario = ruta.itinerario
        return Response(itinerario)


class EscogerRuta(APIView):  # TODO: en implementación
    def post(self, request, *args, **kwargs):
        data = request.data
        rutas = Ruta.objects.filter(transporte__id=data['id'])
        lista = [[r.id, r.fecha_hora] for r in rutas]
        return Response(lista)


class UbicacionDomicilios(APIView):  # TODO: en implementación
    def post(self, request, *args, **kwargs):
        data = request.data
        ruta = Ruta.objects.get(id=data['id'])
        orden = OrdenEntrega.objects.filter(transporte=ruta.transporte, ruta_asig=ruta.id)
        base = orden[0].base
        lista = list()
        geo_base_arg = {"type" : "Feature","geometry" :{"type" : "Point","coordinates" : [float(base.longitud),
                       float(base.latitud)]}, "properties" : {"pos_id": base.pos_id, "nombre" : base.nombre,
                       "direccion": base.direccion, "pais": base.pais, "provincia": base.provincia,
                       "municipio": base.municipio, "consejo_popular": base.consejo_popular, "correo": base.correo,
                       "telefono": base.telefono}}
        lista.append(geo_base_arg)
        for item in orden:
            geo_cliente_arg = {"type" : "Feature","geometry" :{"type" : "Point","coordinates" :
                [float(item.cliente.longitud), float(item.cliente.latitud)]},"properties" :
                {"pos_id": item.cliente.pos_id, "nombre" : item.cliente.nombre, "apellidos": item.cliente.apellidos,
                 "num_ci": item.cliente.num_ci, "direccion": item.cliente.direccion, "telefono": item.cliente.telefono}}
            lista.append(geo_cliente_arg)
        geo_head = {"type" : "FeatureCollection","features" : lista}
        return Response(geo_head)