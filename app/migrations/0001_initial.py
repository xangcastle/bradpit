# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 17:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Categoria')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
                ('identificacion', models.CharField(max_length=14, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=125, null=True)),
                ('direccion', models.TextField(blank=True, max_length=400, null=True)),
                ('limite_credito', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CuentaBanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=30)),
                ('moneda', models.CharField(choices=[('co', 'C$ Cordobas'), ('do', 'U$ Dolares')], default='cordobas', max_length=25)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Banco')),
            ],
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(default=0.0)),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Bodega')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda', models.CharField(choices=[('co', 'C$ Cordobas'), ('do', 'U$ Dolares')], max_length=25, null=True)),
                ('fecha', models.DateTimeField()),
                ('numero', models.PositiveIntegerField(null=True)),
                ('subtotal', models.FloatField(null=True)),
                ('descuento', models.FloatField(null=True)),
                ('excento_iva', models.BooleanField(default=False)),
                ('iva', models.FloatField(null=True)),
                ('aplica_ir', models.BooleanField(default=False)),
                ('ir', models.FloatField(blank=True, null=True)),
                ('numero_ir', models.PositiveIntegerField(blank=True, null=True)),
                ('aplica_al', models.BooleanField(default=False)),
                ('al', models.FloatField(blank=True, null=True, verbose_name='alcaldia')),
                ('numero_al', models.PositiveIntegerField(blank=True, null=True)),
                ('total', models.FloatField(null=True)),
                ('tipopago', models.CharField(choices=[('contado', 'CONTADO'), ('credito', 'CREDITO')], max_length=25, null=True)),
                ('saldo', models.FloatField(null=True)),
                ('impresa', models.BooleanField(default=False)),
                ('cerrada', models.BooleanField(default=False)),
                ('entregada', models.BooleanField(default=False)),
                ('anulada', models.BooleanField(default=False)),
                ('dec_ir', models.BooleanField(default=False)),
                ('dec_al', models.BooleanField(default=False)),
                ('dec_iva', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
                ('short_name', models.CharField(blank=True, max_length=25, null=True)),
                ('no_parte', models.CharField(max_length=25, null=True)),
                ('precio', models.FloatField(blank=True, null=True)),
                ('costo', models.FloatField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('detalles', models.TextField(blank=True, max_length=255, null=True)),
                ('vender', models.BooleanField(default=False)),
                ('comprar', models.BooleanField(default=False)),
                ('almacenar', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Categoria')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True, verbose_name='codigo')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('oficial', models.FloatField()),
                ('venta', models.FloatField(null=True)),
                ('compra', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Sucursal'),
        ),
        migrations.AddField(
            model_name='existencia',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Producto'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Sucursal'),
        ),
    ]
