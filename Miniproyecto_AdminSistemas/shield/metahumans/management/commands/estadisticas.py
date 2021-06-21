from django.core.management import BaseCommand

from metahumans.models import Metahumano, Equipo, Poder

class Command(BaseCommand):
    help = 'Estadisticas de uso de la base de datos'

    def handle(self, *args, **options):
        print("Estaditicas")
        num_equipos = Equipo.objects.count()
        print(f" - Equipos: {num_equipos}")
        num_metahumanos = Metahumano.objects.count()
        print(f" - Metahumanos: {num_metahumanos}")
        num_poderes = Poder.objects.count()
        print(f" - Poderes: {num_poderes}")
