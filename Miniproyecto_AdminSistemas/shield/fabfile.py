import sys
import os
from fabric import Connection, task

PROJECT_NAME = "shield"
PROJECT_PATH = f"~/{PROJECT_NAME}"
REPO_URL = "https://github.com/orsibiro/shield.git"
VENV_PYTHON = f'{PROJECT_PATH}/.venv/bin/python'
VENV_PIP = f'{PROJECT_PATH}/.venv/bin/pip'

@task
def development(ctx):
    ctx.user = 'vagrant'
    ctx.host = '192.168.33.10'
    ctx.connect_kwargs = {"password": "vagrant"}

def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs) as conn:
            return conn
    except Exception as e:
        return None

@task
def clone(ctx):
    print(f"clone repo {REPO_URL}...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    ls_result = conn.run("ls").stdout
    ls_result = ls_result.split("\n")

    if PROJECT_NAME in ls_result:
        print("project already exists")
    else:
        conn.run(f"git clone {REPO_URL} {PROJECT_NAME}")

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

@task
def create_venv(ctx):

    print("Creating venv...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    with conn.cd(PROJECT_PATH):
        conn.run("sudo apt-get install python3-venv")
        conn.run("python3 -m venv .venv")
        conn.run(f"{VENV_PIP} install -r requirements.txt")

@task
def migrate(ctx):
    print("Checking for django db mmigrations...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    
    with conn.cd(PROJECT_PATH):
        conn.run(f"{VENV_PYTHON} manage.py migrate")

@task
def loaddata(ctx):
    print("loading data from fixtures...")

    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    
    with conn.cd(PROJECT_PATH):
        conn.run(f"{VENV_PYTHON} manage.py loaddata metahumans/fixtures/initial_data.json")

        
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
