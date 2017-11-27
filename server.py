"""
Copyright 2017 Alfredo Prado Vega
@radikalbytes
http://www.radikalbytes.com
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0
Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
#Import libraries
import time
import BaseHTTPServer
from pyA20.gpio import gpio
from pyA20.gpio import port
from threading import Thread 
import ConfigParser
import dht22
import time
import datetime
from time import sleep
import os
from meteocalc import Temp, dew_point
import itertools

#Configuracion IP y puerto del servidor
HOST_NAME = '192.168.0.55' # Direccio IP del host
PORT_NUMBER = 80 # Puerto HTTP
#Variables globales
muestras = 0
intervalo = 0
fichero = ""
numeroMaquina = ""
separador = ","
#Carga datos de configuracion del fichero .conf
def cargaConf():
    global muestras
    global intervalo
    global numeroMaquina
    global separador
    global fichero
    config = ConfigParser.ConfigParser()
    config.read('/home/orangepi/armariosServer/armarios.conf')
    muestras = config.get('MUESTRAS','cantidad')
    intervalo = config.get('MUESTRAS','intervalo')
    numeroMaquina = config.get('MAQUINA','numero')
    separador = config.get('FORMATO','separador')
    fichero = config.get('FICHEROS','capturas')
    if separador == "t":
       separador = "\t"
    print ("Configuracion Maquina " + numeroMaquina + " Muestras:  " +  str(muestras) + " Intervalo: " + str(intervalo) )

#Thread del servidor Http
def servidoractivo():
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    subproceso_led.stop()
#Thread heartbreak led rojo
def heartbreak():
    led = port.STATUS_LED
    gpio.init()
    gpio.setcfg(led, gpio.OUTPUT)
    try:
        while True:
            gpio.output(led, 1)
            sleep(0.1)
            gpio.output(led, 0)
            sleep(0.1)

            gpio.output(led, 1)
            sleep(0.1)
            gpio.output(led, 0)
            sleep(0.1)
            sleep(0.6)
    except KeyboardInterrupt:
        print ("Goodbye.")

#Clase Handler de respuesta a peticiones http
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    #Respuesta a un HEAD
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
    #Respuesta al GET
    def do_GET(s):
        global muestras
        global separador
        datosValidos = 0
        """Respond to a GET request."""
        #Muestra valores por consola
        while (datosValidos==0):
            result = instance.read()
            datosValidos = result.is_valid()
        print("Ultima peticion: " + str(datetime.datetime.now()))
        print("Temperatura: %.2f C" % result.temperature)
        print("Humedad: %.2f %%" % result.humidity)
        timestamp = time.strftime("%d/%m/%y %H:%M:%S")
        #Content-type html
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        ffile1 = open(fichero, "r")
        lineas = len(ffile1.readlines())
        #Muestra actual
        temperatura = result.temperature
        humedad = result.humidity
        t = Temp(temperatura,'c')
        pdr = dew_point (temperature = t, humidity = humedad)
        #Si las muestras capturadas no llegan al numero de muestras configuradas
        #Eniva todas 
        if lineas < int(muestras):
            ffile1.seek(0)
            for linea in ffile1:
                s.wfile.write(linea)
            muestra = lineas-1
            linea = (str(muestra)+ separador +timestamp+ separador +str(temperatura)+ separador +str(humedad)+ separador +str(round(pdr,2))+ separador +numeroMaquina+"\n")
            s.wfile.write(linea)
            ffile1.close()
        #Descarta el envio de las muestras anteriores
        else:
           inicioLin = lineas- int(muestras)
           finLineas = lineas-1
           s.wfile.write("muestra"+separador+"timestamp"+separador+"temperatura"+separador+"humedad"+separador+"pdr"+separador+"maquina\n")
           with open(fichero) as data:
               texto = itertools.islice(data,inicioLin, finLineas+1)
               for linea in texto:
                   s.wfile.write(linea)
           muestra = lineas-1
           linea = (str(muestra)+ separador +timestamp+ separador +str(temperatura)+ separador +str(humedad)+ separador +str(round(pdr,2))+ separador +numeroMaquina+"\n")
           s.wfile.write(linea)
           ffile1.close()

if __name__ == '__main__':
    PIN7 = port.PA6  #Pin de datos del DHT22
    gpio.init()      #Inicializa GPIO
    #Carga configuracion en variables globales
    cargaConf() 
    #Si no hay fichero de salida de muestras, crea uno nuevo
    if not os.path.isfile(fichero):
        print ("Creando fichero CSV de muestras")
        ffile = open(fichero,"w")
        ffile.write("muestra"+separador+"timestamp"+separador+"temperatura"+separador+"humedad"+separador+"pdr"+separador+"maquina\n")
        ffile.close()
    #Lee datos sensor en pin 7
    instance = dht22.DHT22(pin=PIN7)
    print("Iniciando servidor HTTP.......")
    #Definicion subproceso servidor http
    subproceso = Thread(target=servidoractivo)
    subproceso_led= Thread(target=heartbreak)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    #Arranque Thread del servidor
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    #Carga hilos, servidor http y heartbreak
    subproceso.start()
    subproceso_led.start()
    #Programa principal
    while (1):
        #Captura muestra
        timestamp = time.strftime("%d/%m/%y %H:%M:%S")
        datosvalidos = 0
        while (datosvalidos==0):
            result = instance.read()
            datosvalidos = result.is_valid()
        ffile = open(fichero,"r")
        muestra = len(ffile.readlines()) - 1
        ffile.close()
        temperatura = result.temperature
        humedad = result.humidity
        t = Temp(temperatura,'c')
        pdr = dew_point (temperature = t, humidity = humedad)
        linea = (str(muestra)+ separador +timestamp+ separador +str(temperatura)+ separador +str(humedad)+ separador +str(round(pdr,2))+ separador +numeroMaquina+"\n")
        print linea,
        ffile = open(fichero,"a")
        ffile.write(linea)
        ffile.close()
        #Temporizacion entre muestras segun intervalo configurado
        sleep(float(intervalo))

