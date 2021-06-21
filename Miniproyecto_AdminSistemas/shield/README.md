# Bienvenida a la applicación de SHIELD para Admin-Sistemas

Pasos a seguir:
1. Haz un fork del proyecto
2. Descarga el proyecto del repo con git
3. Crea un entorno virtual
4. Activa el entorno virtual
5. Instala las librerías del `requirements.txt`
6. Ejecuta las migraciones
7. Carga los datos de superheroes del fichero `superheroes.csv` usando el comando `metahumans/management/commands/load_from_csv.py`. Si os da problemas usando el comando load_from_csv, podéis usar el comando `loaddata` con el fichero `metahumans/fixtures/initial_data.json` 
8. Crea tu propio usuario superuser para poder entrar en el admin de django
9. Ejecuta el servidor de django para probar la aplicación
