import utime as time
import machine
from machine import Pin, Timer
import network
from umqtt.simple import MQTTClient
from settings import *
import neopixel
import ujson as json

# importamos todas las librerìas necesarias
# la conexión wifi se establece en el fichero boot.py
# en settings.py se definen las variables para conectarse al broker: ID, TOPIC, MQTT_SERVER
# el ID siempre tiene que ser único
# el topic al que vamos a suscribirnos es proyectoEOI
# el MQTT_SERVER es un broker público donde se pueden hacer pruebas

class DomoticLight:                                        # creamos la clase
    hay_que_enviar = False
    def __init__(self):
        self.led = neopixel.NeoPixel(machine.Pin(27), 1)   # en el constructor configuramos el botón y el led
        self.boton = machine.Pin(39, machine.Pin.IN)
        self.mqtt_config()
        self.run()
        
    def mqtt_config(self):                                 # Configuramos el MQTT
        self.client = MQTTClient(ID, MQTT_SERVER)          # le pasamos el ID y el MQTT_SERVER
        self.client.set_callback(self.mqtt_cb)             # cuando entren mensajes por los topics a los que estamos suscritos, dispara el callback
        self.client.connect()
        self.client.subscribe(TOPIC)                       # le pasamos el topic al que queremos suscribirnos
        self.enviar_msg()

    def run(self):                                              # la función que nos permitirá enviar y recibir mensajes
        print("Listening on topic: {}".format(TOPIC.decode()))
        while True:
            self.client.check_msg()                        # combrueba los mensajes
            if not self.boton.value():
                self.client.publish(TOPIC, b"hola soy Orsi")  # al pulsar el botón enviamos el mensaje
                time.sleep_ms(500)                            # le damos una pausa para que no publique varios mensajes seguidos

    def enviar_msg(self):
        global hay_que_enviar
        hay_que_enviar = True

    
    def mqtt_cb(self, topic, msg,):            # Cuando hacemos check_msg() y hay mensajes en los topics a los que estamos suscritos entra aqui
        msg = msg.decode().lower()             # son arrays de bytes, lo pasamos a string
        topic = topic.decode()

        try:                                  
            msg_dict = json.loads(msg)                                       # transformamos en mensaje de string a un diccionario
            print("")
            print("I got from '{}' this: '{}' ".format(topic, msg))          # imprimimos por la consola el mensaje que ha llegado
        
            msg_list = (msg_dict["red"],msg_dict["green"],msg_dict["blue"])   # del diccionario solo nos quedaremos con los números que indicarán
                                                                              # el color que tiene que adoptar el led
            self.led[0] = msg_list
            self.led.write()
        except ValueError:                                                    # si el mensaje no tiene el formato y la información que necesitamos
            pass                                                              # no hace nada y sigue esperando más mensajes

domoticlight = DomoticLight()       
domoticlight.run()