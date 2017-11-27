"""
Copyright 2017 Alfredo Prado Vega
@radikalbytes
http://www.radikalbytes.com
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0
Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import time
import ConfigParser

def main():
    print("""

                  Configuracion de Muestras y capturas


         """)
    config = ConfigParser.RawConfigParser()
    #/home/orangepi/armariosServer/
    config.read('/home/orangepi/armariosServer/armarios.conf')
    muestras = config.get('MUESTRAS','cantidad')
    intervalo = config.get('MUESTRAS','intervalo')
    numeroMaquina = config.get('MAQUINA','numero')
    separador = config.get('FORMATO','separador')
    fichero = config.get('FICHEROS','capturas')
    #Configura numero de muestras a devolver
    print("Introduce numero de Muestras a enviar")
    print("Muestras actuales: "+str(muestras))
    print("Presiona Enter para mantener el valor")
    tmpInput =raw_input();
    if not tmpInput=="":
        print ("El nuevo valor de muestras a mostrar es: "+tmpInput)
        config.set('MUESTRAS','cantidad',str(tmpInput))
    #Configura intervalo
    print("\n\n\nIntroduce intervalo en segundos entre muestras")
    print("Intervalo actual: "+str(intervalo)+" segundos")
    print("Presiona Enter para mantener el valor")
    tmpInput = raw_input();
    if not tmpInput=="":
        print ("El nuevo intervalo entre muestras es: "+tmpInput)
        config.set('MUESTRAS','intervalo',str(tmpInput))
    #Configura Nombre de Maquina
    print("\n\n\nIntroduce Nombre de Maquina (Ex: WQ2533)")
    print("Maquina actual: "+str(numeroMaquina))
    print("Presiona Enter para mantener el valor")
    tmpInput = raw_input();
    if not tmpInput=="":
        print ("El nuevo nombre de Maquina es: "+tmpInput)
        config.set('MAQUINA','numero',str(tmpInput))
    #Configura separador CSV
    print("\n\n\nIntroduce tipo de separador CSV (t=tabulacion)")
    print("Separador actual: "+str(separador))
    print("Presiona Enter para mantener el valor")
    tmpInput = raw_input();
    if not tmpInput=="":
        print ("El nuevo separador CSV es: "+tmpInput)
        config.set('FORMATO','separador',str(tmpInput))
    #Configura nombre fichero capturas
    print("\n\n\nIntroduce nombre de fichero de capturas (sin ruta)")
    print("Fichero actual: "+str(fichero))
    print("Presiona Enter para mantener el valor")
    tmpInput = raw_input();
    if not tmpInput=="":
        print ("El nuevo fichero de capturas es: "+tmpInput)
        config.set('FICHEROS','capturas',"/home/orangepi/armariosServer/"+str(tmpInput))

    ffile = open('/home/orangepi/armariosServer/armarios.conf',"w")
    config.write(ffile)
    ffile.close()

if __name__ == '__main__':
    sys.exit(main())

