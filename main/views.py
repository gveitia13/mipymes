import json
from datetime import datetime

import pandas as pd
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Enterprise, Sector, Provincia, Municipio, Service, Enlace


def cargar_empresas(request):
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_excel')
        data = pd.read_excel(archivo_excel)
        empresas = Enterprise.objects.all()
        all_municipios = Municipio.objects.all()
        for index, row in data.iterrows():
            print(row['municipio'])
            try:
                municipio = all_municipios.get(nombre__iexact=row['municipio'])
            except:
                municipios = all_municipios.filter(nombre__icontains=row['municipio'])
                for m in municipios:
                    if m.provincia.nombre.__contains__(row['provincia']):
                        municipio = m
                        break

            representante = row.get('representante', None)
            telefono = row.get('telefono', None)
            correo = row.get('correo', None)
            fecha_aprobacion = row.get('fecha_aprobacion', None)
            if fecha_aprobacion:
                try:
                    fecha_aprobacion = datetime.strptime(fecha_aprobacion, '%Y-%m-%d %H:%M:%S')
                except:
                    fecha_aprobacion = None

            if empresas.filter(nombre=row['nombre']).exists():
                empresa = empresas.get(nombre=row['nombre'])
                empresa.nombre = row['nombre']
                empresa.municipio = municipio
                empresa.actividad = row['actividad']
                empresa.representante = representante
                empresa.telefono = telefono
                empresa.correo = correo
                empresa.fecha_aprobacion = fecha_aprobacion
                empresa.is_active = True
                empresa.save()
            else:
                empresa = Enterprise.objects.create(nombre=row['nombre'], municipio=municipio,
                                                    actividad=row['actividad'], representante=representante,
                                                    telefono=telefono, correo=correo, fecha_aprobacion=fecha_aprobacion,
                                                    is_active=True, )
            servicios = json.loads(row['servicios'])
            for s in servicios:
                Service.objects.create(servicio=s, enterprise=empresa)

            enlaces = json.loads(row['enlaces'])
            if len(enlaces):
                for e in enlaces:
                    Enlace.objects.create(nombre=e[0], enlace=e[1], enterprise=empresa)

            sectores = json.loads(row['sectores'])
            if sectores:
                for s in sectores:
                    sector = Sector.objects.get(sector=s)
                    empresa.sectores.add(sector)
        return redirect('/admin/main/enterprise/')
    return render(request, 'cargar_excel.html')


def cargar_sectores(request):
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_excel')
        data = pd.read_excel(archivo_excel)
        sectores = Sector.objects.all()
        for index, row in data.iterrows():
            for sector in json.loads(row['sectores']):
                if not sectores.filter(sector=sector).exists():
                    Sector.objects.create(sector=sector)
        return redirect('/admin/main/sector/')
    return render(request, 'cargar_excel.html')


def cargar_provincias(request):
    if request.method == 'POST':
        archivo_excel = request.FILES.get('archivo_json')
        data = json.load(archivo_excel)
        print(data['Provincias'])
        for p in data['Provincias']:
            if not Provincia.objects.filter(nombre=p['nombre']).exists():
                provincia = Provincia.objects.create(nombre=p['nombre'])
            else:
                provincia = Provincia.objects.get(nombre=p['nombre'])
            if p.get('municipios') is not None:
                for m in p['municipios']:
                    if not Municipio.objects.filter(nombre=m).exists():
                        municipio = Municipio.objects.create(nombre=m, provincia=provincia)
        return redirect('/admin/main/provincia/')
    return render(request, 'cargar_excel.html')
