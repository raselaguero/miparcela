from django.contrib import admin
from .models import Parcela, Transporte, Obrero, Agricultor, OrdenEntrega, Cultivo, Ruta, PaqueteSemillas, Imagen, Celda
# Register your models here.

admin.site.register(Parcela)
admin.site.register(Transporte)
admin.site.register(Obrero)
admin.site.register(Agricultor)
admin.site.register(OrdenEntrega)
admin.site.register(Cultivo)
admin.site.register(PaqueteSemillas)
admin.site.register(Imagen)
admin.site.register(Celda)
admin.site.register(Ruta)
