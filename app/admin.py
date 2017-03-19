from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import site
import adminactions.actions as actions
actions.add_to_site(site)
from .models import *

class entidad_admin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    fields = ('name', 'code')

class tasa_de_cambio(ImportExportModelAdmin):
    date_hierarchy = 'fecha'
    list_display = ('fecha', 'oficial', 'compra', 'venta')
admin.site.register(TC, tasa_de_cambio)
admin.site.register(Banco, entidad_admin)
class cuentas_de_banco(admin.ModelAdmin):
    list_display = ('numero', 'moneda', 'banco')
    list_filter = ('banco',)
admin.site.register(CuentaBanco, cuentas_de_banco)
class cartera_clientes(ImportExportModelAdmin):
    list_display = ('code', 'name', 'identificacion', 'telefono', 'limite_credito')
    fields = (('name', 'code'), ('identificacion', 'telefono'),
              'direccion', 'limite_credito')
admin.site.register(Cliente, cartera_clientes)
