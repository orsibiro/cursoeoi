import hashlib
import os
import argparse
from hashlib import md5
import time
import datetime
import shutil
import logging
from playsound import playsound

parser = argparse.ArgumentParser()
parser.add_argument('path', help="La ruta del fichero del que quieres hacer la copia de seguridad")
parser.add_argument('-e', '--exclude', help="Extensiones de ficheros que quieres excluir de la copia de seguridad")
parser.add_argument('-v', '--verbose', action='store_true', help="Imprimir código hash MD5 y nombre del fichero")
args = parser.parse_args()
path = args.path

datetoday = datetime.date.today().weekday()
date_log = datetime.datetime.now()
logging.basicConfig(filename='weeko.log', level=logging.DEBUG)

def crear_carpetas(d):
    if d == 0:
        if not os.path.isdir("./lunes"):
            os.mkdir("./lunes", mode=0o755)
            backup_path = "./lunes"
        else:
            backup_path = "./lunes"
    elif d == 1:
        if not os.path.isdir("./martes"):
            os.mkdir("./martes", mode=0o755)
            backup_path = "./martes"
        else:
            backup_path = "./martes"
    elif d == 2:
        if not os.path.isdir("./miercoles"):
            os.mkdir("./miercoles", mode=0o755)
            backup_path = "./miercoles"
        else:
            backup_path = "./miercoles"
    elif d == 3:
        if not os.path.isdir("./jueves"):
            os.mkdir("./jueves", mode=0o775)
            backup_path = "./jueves"
        else:
            backup_path = "./jueves"
    elif d == 4:
        if not os.path.isdir("./viernes"):
            os.mkdir("./viernes", mode=0o755)
            backup_path = "./viernes"
        else:
            backup_path = "./viernes"  
    elif d == 5:
        if not os.path.isdir("./sabado"):
            os.mkdir("./sabado", mode=0o755)
            backup_path = "./sabado"
        else:
            backup_path = "./sabado"
    elif d == 6:
        if not os.path.isdir("./domingo"):
            os.mkdir("./domingo", mode=0o755)
            backup_path = "./domingo"
        else:
            backup_path = "./domingo"
    return backup_path

bu_path = crear_carpetas(datetoday)
origin = os.listdir(path)

with open('weeko.log', 'a') as l:
    for file in origin:
        filepath = path + '/'+ file
        file_bupath = bu_path + '/' + file
        if args.exclude:
            excluded_files = args.exclude.split(',')
            for extension in excluded_files:
                if extension not in file:
                    shutil.copyfile(filepath, file_bupath)
                    with open(filepath, "rb") as f:
                        bytes = f.read()
                        readable_hash = hashlib.md5(bytes).hexdigest()
                        l.write(f"{date_log.year}-{date_log.month}-{date_log.day} {date_log.hour:02}:{date_log.minute:02}:{date_log.second:02}: Copia de {filepath} (MD5 {readable_hash}) a la carpeta {bu_path}" + '\n')
                        if args.verbose:
                            print(readable_hash)
        else:
            shutil.copyfile(filepath, file_bupath)
            with open(filepath, "rb") as f:
                bytes = f.read()
                readable_hash = hashlib.md5(bytes).hexdigest()
                l.write(f"{date_log.year}-{date_log.month}-{date_log.day} {date_log.hour:02}:{date_log.minute:02}:{date_log.second:02}: Copia de {filepath} (MD5 {readable_hash}) a la carpeta {bu_path}" + '\n')
                if args.verbose:
                    print(readable_hash)
        
playsound('nokia-tune.mp3')


    

