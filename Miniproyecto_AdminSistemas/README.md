# Bienvenid@ al Miniproyecto del módulo Administración de Sistemas

Este miniproyecto consiste en descargar el proyecto SHIELD que habíamos preparado durante el módulo Desarrollo Web, y desplegarlo en una máquina virtual.

## Pasos para instalar la applicación SHIELD en tu máquina local:

1. Haz un fork del proyecto desde este repositorio:
```
https://github.com/orsibiro/shield
```
2. Descarga el proyecto del repositorio con el siguiente comando:
```
git clone https://github.com/orsibiro/shield.git
```
3. Entra en la carpeta `shield` y crea el entorno virtual:
```
cd shield
python3 -m venv .venv
```
4. Activa el entorno virtual:
```
source .venv/bin/activate
```
5. Instala las librerías necesarias que se encuentran en el fichero `requirements.txt`
```
pip install -r requirements.txt
```
6. Ejecuta las migraciones:
```
python3 manage.py migrate
```
7. Carga los datos del fichero `superheroes.csv`
```
python3 manage.py metahumans/management/commands/load_from_csv.py
```
*Si con este comando no te funciona, puedes utilizar el comando `loaddata`:
```
python3 manage.py loaddata metahumans/fixtures/initial_data.json
```
8. Configura localhost como IP permitida para django. Edita el fichero `shield/settings.py`. Añade la IP local a la variable `ALLOWED_HOSTS` (en la línea 28) de forma que quede así:
```
ALLOWED_HOSTS = ['192.168.33.10', '127.0.0.1']
```
9. Crea tu propio usuario superuser para poder entrar en el admin de django
```
python3 manage.py createsuperuser
Username: admin
Email address: admin@example.com
```
10. Ejecuta el servidor de django para probar la aplicación:
```
python3 manage.py runserver
```
## Pasos para instalar el proyecto en una máquina remota con Fabric

1. Instala la librería de Fabric:
```
pip install fabric
```
2. Crea el fichero `fabfile.py` y haz los imports:
```
import sys
import os
from fabric import Connection, task
```
3. Define las variables que utilizarás como constantes en el despliegue de la aplicación:
```
PROJECT_NAME = "shield"
PROJECT_PATH = f"~/{PROJECT_NAME}"
REPO_URL = "https://github.com/orsibiro/shield"
VENV_PYTHON = f'{PROJECT_PATH}/.venv/bin/python'
VENV_PIP = f'{PROJECT_PATH}/.venv/bin/pip'
```

3. Crea una tarea para ajustar la IP del servidor remoto y las credenciales en las líneas 11-15 del script `fabfile.py` de este modo:
```
@task
def development(ctx):
    ctx.user = 'vagrant'
    ctx.host = '192.168.33.10'
    ctx.connect_kwargs = {"password": "vagrant"}
```
3. Crea una función para establecer la conexión usando los parámetros introducidos en la tarea anterior. De este modo podrás reutilizar esta función en otras tareas más adelante.
```
def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs) as conn:
            return conn
    except Exception as e:
        return None
```
4. Crea una tarea `deploy`. Esta tarea realizará el despliegue de la aplicación en la máquina de vagrant.
```
@task
def deploy(ctx):
    conn = get_connection(ctx)
    if conn is None:
        sys.exit("Failed to get connection")
```
Ahora veremos las tareas que debes crear para ejecutar ahora de forma automática los mismos pasos que ya habías realizado en tu máquina local.

- Tarea para el `git clone`:
```
@task
def clone(ctx):
    print(f"clone repo {REPO_URL}...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    # obtengo las carpetas del directorio
    ls_result = conn.run("ls").stdout

    # divido el resultado para tener cada carpeta en un objeto de una lista
    ls_result = ls_result.split("\n")

    # si el nombre del proyecto ya está en la lista de carpetas
    # no es necesario hacer el clone
    if PROJECT_NAME in ls_result:
        print("project already exists")
    else:
        conn.run(f"git clone {REPO_URL} {PROJECT_NAME}")
```
- Tarea para hacer un checkout de la rama `main` del repositorio:
```
@task
def checkout(ctx, branch=None):
    print("Checkout to branch {branch}...")

    if branch is None:
        sys.exit("branch name is not specified")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    with conn.cd(PROJECT_PATH):
        conn.run(f"git checkout {branch}")
```
- Tarea para hacer un `git pull` de la rama:
```
@task
def pull(ctx, branch="main"):

    print(f"Pulling latest code from {branch} branch...")

    if branch is None:
        sys.exit("Branch name is not specified")
    
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    
    with conn.cd(PROJECT_PATH):
        conn.run(f"git pull origin {branch}")
```
- Tarea para crear un entorno virtual e instalar las librerìas necesarias del arcivo `requirements.txt`:
```
@task
def create_venv(ctx):

    print("Creating venv...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    with conn.cd(PROJECT_PATH):
        conn.run("python3 -m venv .venv")
        conn.run(f"{VENV_PIP} install -r requirements.txt")
```
- Tarea para ejecutar las migraciones de django:
```
@task
def migrate(ctx):
    print("Checking for django db mmigrations...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    
    with conn.cd(PROJECT_PATH):
        conn.run(f"{VENV_PYTHON} manage.py migrate")
```

5. Añade todas las tareas creadas a la función `deploy`. Tiene que quedar así:
```
@task
def deploy(ctx):
    conn = get_connection(ctx)
    if conn is None:
        sys.exit("Failed to get connection")
    
    clone(conn)
    checkout(conn, branch="main")
    pull(conn, branch="main")
    create_venv(conn)
    migrate(conn)
    loaddata(conn)
```
6. Ejecuta el script con el siguiente comando:
```
fab development deploy
```
## Pasos para aprovisionar una máquina y desplegar el proyecto con Ansible

1. Instala Ansible en tu sistema operativo:
```
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
```
2. Instala la librería de Ansible con PIP:
```
pip install ansible
```
3. Crea una carpeta `ansible` dentro del proyecto.

4. Crea un fichero llamado `hosts` dentro de la carpeta `ansible`

5. Crea un fichero `vars.yml`

6. Crea un fichero `provision.yml`

7. Crea un fichero `deploy.yml`

8. Dentro de la carpeta `ansible` ejecuta el siguiente comando:
```
ansible-playbook -i hosts provision.yml --user=vagrant --ask-pass
```
9. Dentro de la carpeta `ansible` ejecuta el siguiente comando:
```
ansible-playbook -i hosts deploy.yml --user=vagrant --ask-pass
```
10. 

## Pasos para la dockerización del proyecto
Antes que nada tienes que instalar Docker en tu ordenador y asegurarte de que tienes la versión 2 de WSL si utilizas Windows.

1. Como primer paso tienes que asegurarte de que tu aplicación funciona a nivel local. Para eso dentro de la carpeta del proyecto ejecuta el siguiente comando:
```
python manage.py runserver
```
2. Si has comprobado que tu aplicación funciona el siguiente paso es que crees un archivo con el nombre `Dockerfile`
- La primera línea de este archivo es la directiva de sintaxis. No es obligatorio ponerlo, pero no viene mal si está.
```
# syntax=docker/dockerfile:1
```
- Después tienes que poner el software base del que vamos a partir. En este caso es uno que ya tiene las librerías de Python instaladas.
```
FROM python:3.9-slim-buster
```
- Define en qué carpeta quieres guardar el código dentro de Docker.
```
WORKDIR /app
```
- Para asegurarte de que el contenedor Docker sea lo más ligero posible solo tendrás que instalar el fichero `requirements.txt` para tener todo lo necesario para el proyecto. (Siempre asegurándote de que la applicación funciona en local)
```
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
```
- Si ya tienes insatalado todos los `requirements` copia todos los ficheros del código del proyecto con el siguiente comando:
```
COPY . .
```
- Ejecuta el runserver en Docker de la siguiente manera:
```
CMD [ "python3", "manage.py", "runserver", "127.0.0.1:8000"]
```

3. Ejecuta el comando para crear la imagen de Docker:
```
docker build . --tag shield
```
4. Con el comando `docker images` puedes comprobar si se ha creado bien la imagen de Docker.

5. Ejecuta la imagen con el comando: 
```
docker run --publish 8000:8000 shield
curl localhost:8000
```
6. Con el comando `docker ps` puedes comprobar qué contenedores se están ejecutando en tu máquina.

## Movidas durante el proyecto
1. Para la primera parte del proyecto tuve que usar la versión 1 de wsl porque con la 2 vagrant no funciona, sin embargo, para la parte de Docker hay que utilizar la versión 2 porque con la otra éste no funciona.
