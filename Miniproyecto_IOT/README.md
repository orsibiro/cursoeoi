# Como miniproyecto para la parte de IOT, vamos a desarrollar una “luz domótica”, que funcione a través de MQTT.

A grandes rasgos, cambiaremos el color del led RGB según los mensajes MQTT que recibamos.

## Requisitos
- El broker MQTT será ‘broker.hivemq.com’
- El topic al que nos suscribimos será ‘proyectoEOI’
- Por el topic recibiremos mensajes en formato JSON del tipo { “red”: 255, “green”: 255, “blue”: 255}
- Cuando llegue un mensaje, cambiamos el color del led según estos valores
- Los mensajes que no esten en formato json o que no contengan las 3 claves red, green y blue, se descartan (no hacemos nada)


## Estructura de ficheros
- El proyecto contará con 3 ficheros:

    * Un fichero de configuración “credenciales.py” donde le especifiquemos el nombre y password de nuestra wifi (este fichero no se entrega cuando enviemos el proyecto)
    * Un fichero boot.py que se encargue de conectarse a la wifi en modo station. (no es necesario subirlo)
    * Un fichero main.py donde esté el superloop (while 1) que compruebe periódicamente los mensajes que lleguen por MQTT y realice las acciones correspondientes


## Criterios de evaluación
- Funcionalidad: El código hace lo que se pide sin errores
    * 60 puntos si al recibir un mensaje cambia el color del led
- Estructura y comentarios
    * 15 puntos por encapsular las funcionalidades en clases (crear la clase en el mismo fichero main.py)
    * 10 puntos comentar correctamente todas las partes
- Funcionalidades adicionales
    * 15 Puntos por incluir alguna funcionalidad extra (publicar con el botón, encender el led infrarojo....)

## Forma de entrega
Se subirá a Google Classroom solo el main.py. IMPORTANTE: Los datos personales como nombre de la wifi y clave de la wifi los tendremos a parte en un fichero “credenciales.py” y ese fichero no se sube

## Validación
Se comprobará que el programa funciona entrando al cliente MQTT de
hivemq (enlace debajo) y publicando por el canal
proyectoEOI  los siguientes mensajes:

- { “red”: 255, “green”: 255, “blue”: 255}
- { “red”: 0, “green”: 0, “blue”: 255  }
- { “red”: 32, “green”:    128, “blue”: 64}
- { “red”: 0,“green”:0,“blue”: 0}

http://www.hivemq.com/demos/websocket-client/