#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

from django.core.management.base import BaseCommand, CommandError

from metahumans.models import Equipo, Poder, Metahumano


class Command(BaseCommand):
    help = 'Rellena la base de datos a partir de un fichero CSV'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def error_file_not_exists(self, filename):
        raise CommandError(f"No existe el fichero f{filename}")

    def handle(self, *args, **options):
        filename = options.get('filename')
        if not os.path.exists(filename):
            self.error_file_not_exists(filename)
        print(f"Importando metahumanos desde {filename}")
        with open(filename, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            counter = 0
            for (nombre, identidad, nivel, equipo, cuartel, poderes) in reader:
                print(f" - Creando metahumano {nombre}", end=' ', flush=True)
                if Metahumano.objects.filter(nombre=nombre).exists():
                    print("[skipped]")
                    continue
                metahumano = Metahumano(
                    nombre=nombre,
                    identidad=identidad,
                    nivel=int(nivel),
                    )
                equipo = equipo.title().strip()
                if equipo:
                    su_equipo, _ = Equipo.objects.get_or_create(
                        nombre=equipo,
                        cuartel=cuartel,
                        )
                    metahumano.equipo = su_equipo
                set_poderes = set([])
                for nombre_poder in poderes.split(","):
                    nombre_poder = nombre_poder.strip().lower()
                    poder, _ = Poder.objects.get_or_create(nombre=nombre_poder)
                    set_poderes.add(poder)
                    print(".", end="", flush=True)
                metahumano.save()
                metahumano.poderes.set(set_poderes)
                metahumano.save()
                counter += 1
                print("[ok]")
        print(f"Importados {counter} metahumanos a la base de datos")
