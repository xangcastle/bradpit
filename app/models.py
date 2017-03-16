from __future__ import unicode_literals
from .base import Entidad
from django.db import models
from datetime import datetime


MONEDAS = (("co", "C$ Cordobas"), ("do", "U$ Dolares"))
TIPOS_PAGO = (("contado", "CONTADO"), ("credito", "CREDITO"))

class TC(models.Model):
    fecha = models.DateField()
    oficial = models.FloatField()
    venta = models.FloatField(null=True)
    compra = models.FloatField(null=True)

def dolarizar(cordobas=1, fecha=datetime.now(), digitos=2):
    tc = TC.objects.get(fecha__year=fecha.year, fecha__month=fecha.month,
        fecha__day=fecha.day)
    if tc.venta and tc.venta > tc.oficial:
        tc = tc.venta
    else:
        tc = tc.oficial
    return round(cordobas / tc, digitos)

def cordobizar(dolares=1, fecha=datetime.now(), digitos=2):
    tc = TC.objects.get(fecha__year=fecha.year, fecha__month=fecha.month,
        fecha__day=fecha.day)
    if tc.compra and tc.compra < tc.oficial:
        tc = tc.compra
    else:
        tc = tc.oficial
    return round(dolares * tc, digitos)

class Banco(Entidad):
    pass

class CuentaBanco(models.Model):
    banco = models.ForeignKey(Banco)
    numero = models.CharField(max_length=30)
    moneda = models.CharField(max_length=25, default="cordobas", choices=MONEDAS)

    def __unicode__(self):
        return "%s %s- %s" % (self.banco.name, self.moneda, self.numero)

class Sucursal(Entidad):
    pass

class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal)

class datos_generales(models.Model):
    identificacion = models.CharField(max_length=14, null=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=125, null=True, blank=True)
    direccion = models.TextField(max_length=400, null=True, blank=True)

    class Meta:
        abstract = True


class Cliente(Entidad, datos_generales):
    limite_credito = models.FloatField(default=0.0)

    def facturas(self):
        return Factura.objects.filter(cliente=self, impresa=True, saldo__gt=0.0)

    def saldo(self):
        data = {}
        cordobas =  self.facturas().filter(moneda="cordobas")
        dolares =  self.facturas().filter(moneda="dolares")
        if cordobas.count() > 0:
            data['cordobas'] = cordobas.aggregate(Sum('saldo'))['saldo__sum']
        else:
            data['cordobas'] = 0.0
        if dolares.count() > 0:
            data['dolares'] = dolares.aggregate(Sum('saldo'))['saldo__sum']
        else:
            data['dolares'] = 0.0
        data['total_cordobas'] = cordobizar(data['dolares']) + data['cordobas']
        data['total_dolares'] = dolarizar(data['cordobas']) + data['dolares']
        return data

    def saldo_disponible(self):
        return self.limite_credito - (self.saldo()['cordobas'] + cordobizar(self.saldo()['dolares']))

    def ecuenta(self):
        data = []
        facturas = Factura.objects.filter(cliente=self, impresa=True)
        for f in facturas:
            if f.moneda == "cordobas":
                data.append({'fecha': f.date,
                'referencia': "F - " + str(f.numero),
                'descripcion': "Factura Numero " + str(f.numero),
                'cordobas': f.total,
                'dolares': 0.0})
                if f.aplica_ir:
                    print("aplica ir")
                    data.append({'fecha': f.date,
                    'referencia': "IR - " + str(f.numero_ir),
                    'descripcion': "Retencion en la Fuente # " + str(f.numero_ir),
                    'cordobas': -f.ir,
                    'dolares': 0.0})
                if f.aplica_al:
                    data.append({'fecha': f.date,
                    'referencia': "AL - " + str(f.numero_al),
                    'descripcion': "Retencion Alcaldia Municipal # " + str(f.numero_al),
                    'cordobas': -f.al,
                    'dolares': 0.0})
            else:
                data.append({'fecha': f.date,
                'referencia': "F - " + str(f.numero),
                'descripcion': "Factura Numero " + str(f.numero),
                'dolares': f.total,
                'cordobas': 0.0})
                if f.aplica_ir:
                    print("aplica ir")
                    data.append({'fecha': f.date,
                    'referencia': "IR - " + str(f.numero_ir),
                    'descripcion': "Retencion en la Fuente # " + str(f.numero_ir),
                    'dolares': -f.ir,
                    'cordobas': 0.0})
                if f.aplica_al:
                    data.append({'fecha': f.date,
                    'referencia': "AL - " + str(f.numero_al),
                    'descripcion': "Retencion Alcaldia Municipal # " + str(f.numero_al),
                    'dolares': -f.al,
                    'cordobas': 0.0})
        abonos = Roc.objects.filter(cliente=self)
        for a in abonos:
            if a.moneda == "cordobas":
                data.append({'fecha': a.fecha,
                'referencia': "ROC - " + str(a.numero),
                'descripcion': a.concepto,
                'dolares': 0.0,
                'cordobas': -a.monto})
            else:
                data.append({'fecha': a.fecha,
                'referencia': "ROC - " + str(a.numero),
                'descripcion': a.concepto,
                'cordobas': 0.0,
                'dolares': -a.monto})
        data = sorted(data, key=lambda doc: doc['fecha'], reverse=False)
        return data

    def to_json(self):
        obj = super(Cliente, self).to_json()
        obj['facturas'] = []
        for f in self.facturas():
            obj['facturas'].append(f.to_json())
        obj['saldo'] = self.saldo()
        obj['saldo_disponible'] = self.saldo_disponible()
        return obj

class Categoria(Entidad):
    parent = models.ForeignKey('self', null=True, blank=True)


class Producto(Entidad):
    categoria = models.ForeignKey(Categoria, null=True)
    short_name = models.CharField(max_length=25, null=True, blank=True)
    no_parte = models.CharField(max_length=25, null=True)
    precio = models.FloatField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True)
    detalles = models.TextField(max_length=255, null=True, blank=True)
    vender = models.BooleanField(default=False)
    comprar = models.BooleanField(default=False)
    almacenar = models.BooleanField(default=False)


class Existencia(models.Model):
    bodega = models.ForeignKey(Bodega)
    producto = models.ForeignKey(Producto)
    cantidad = models.FloatField(default=0.0)


class Factura(models.Model):
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True)
    moneda = models.CharField(max_length=25, null=True, choices=MONEDAS)
    fecha = models.DateTimeField()
    numero = models.PositiveIntegerField(null=True)
    cliente = models.ForeignKey(Cliente, null=True)
    subtotal = models.FloatField(null=True)
    descuento = models.FloatField(null=True)

    excento_iva = models.BooleanField(default=False)
    iva = models.FloatField(null=True)

    aplica_ir = models.BooleanField(default=False)
    ir = models.FloatField(null=True, blank=True)
    numero_ir = models.PositiveIntegerField(null=True, blank=True)

    aplica_al = models.BooleanField(default=False)
    al = models.FloatField(null=True, verbose_name="alcaldia", blank=True)
    numero_al = models.PositiveIntegerField(null=True, blank=True)

    total = models.FloatField(null=True)
    tipopago = models.CharField(max_length=25, null=True, choices=TIPOS_PAGO)
    saldo = models.FloatField(null=True)

    impresa = models.BooleanField(default=False)
    cerrada = models.BooleanField(default=False)
    entregada = models.BooleanField(default=False)
    anulada = models.BooleanField(default=False)
    dec_ir = models.BooleanField(default=False)
    dec_al = models.BooleanField(default=False)
    dec_iva = models.BooleanField(default=False)


