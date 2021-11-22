from django.urls import path
from Atajo import views
from rest_framework.authtoken.views import obtain_auth_token
#from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework.authtoken import views


urlpatterns = [
    path('', views.RegisterView.as_view(), name='register_view'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('obreros/', views.ObreroLista.as_view(), name='obreros_lista'),
    path('obreros/<int:pk>/', views.ObreroDetalle.as_view(), name='obreros_detalle'),
    path('cultivos/', views.CultivoLista.as_view(), name='cultivos_lista'),
    path('cultivos_c/', views.CultivoCrear.as_view(), name='cultivos_crear'),
    path('cultivos/<int:pk>/', views.CultivoDetalle.as_view(), name='cultivos_detalle'),
    path('transportes/', views.TransporteLista.as_view(), name='transportes_lista'),
    path('transportes/<int:pk>/', views.TransporteDetalle.as_view(), name='transportes_detalle'),
    path('agricultores/', views.AgricultorLista.as_view(), name='agricultores_lista'),
    path('agricultores/<int:pk>/', views.AgricultorDetalle.as_view(), name='agricultores_detalle'),
    path('ordenes_entrega/', views.OrdenEntregaLista.as_view(), name='ordenes_entrega_lista'),
    path('ordenes_entrega/<int:pk>/', views.OrdenEntregaDetalle.as_view(), name='ordenes_entrega_detalle'),
    path('parcelas/', views.ParcelaLista.as_view(), name='parcelas_lista'),
    path('parcelas/<int:pk>/', views.ParcelaDetalle.as_view(), name='parcelas_detalle'),
    path('paquete_semillas/', views.PaqueteSemillasLista.as_view(), name='paquete_semillas_lista'),
    path('paquete_semillas/<int:pk>/', views.PaqueteSemillasDetalle.as_view(), name='paquete_semillas_detalle'),
    path('usuarios/', views.UserLista.as_view(), name='usuarios_lista'),
    path('usuarios/<int:pk>/', views.UserDetalle.as_view(), name='usuarios_detalle'),
    path('ubicacion/', views.Ubicacion.as_view(), name='ubicacion'),
    path('escoger_ruta/', views.EscogerRuta.as_view(), name='escoger_ruta'),
    path('ruta/', views.Trazo.as_view(), name='ruta'),
    path('ubicacion_domicilios/', views.UbicacionDomicilios.as_view(), name='ubicacion_domicilios')
]
#urlpatterns = format_suffix_patterns(urlpatterns)