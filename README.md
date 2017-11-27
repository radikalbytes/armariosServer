# Ayuda

Programa servidor http de datos CSV para monitorizacion
de temperatura, humedad y punto de rocio de armarios
electricos industriales.

El programa server.py se carga automáticamente en el arranque de la maquina Linux.

Estará operativo en el momento en el que el led rojo de la placa efectue la
simulacion de un latido de corazon.


### Conexion por SSH:
`ssh root@<IP>`
`password: gkn`

### En la consola:
`$ configura`    --- Inicia el programa de configuracion

      1. Numero de muestras a enviar
      2. Intervalo en segundos entre muestras
      3. Nombre de la maquina
      4. Tipo de separador CSV (t=tabulador)
      5. Nombre de fichero de captura

### Cambio de direccion IP, Gateway y Netmask:
Editar `/etc/network/interfaces` con 
```sh 
sudo nano /etc/network/interfaces
```
##### Configuración básica:

        # interfaces(5) file used by ifup(8) and ifdown(8)
        # Include files from /etc/network/interfaces.d:
        source-directory /etc/network/interfaces.d
        auto lo
        iface lo inet loopback
        auto eth0
        iface eth0 inet static
        address 192.168.0.55
        netmask 255.255.0.0
        gateway 192.168.0.1

Y en fichero `/etc/dhpcd.conf` configurar valores de DNS y DHCP
Editar `/etc/dhpcd.conf` con 
```sh
sudo nano /etc/dhpcd.conf
```
##### Configuracion basica:

       interface eth0
       static ip_address=192.168.0.55/24
       static routers=192.168.0.1
       static domain_name_servers=192.168.0.1

Comandos Linux de ayuda:
```sh
  - Ver direccion IP, Gateway y Netmask:    $ ifconfig
  - Listar procesos:                        $ ps
  - Listar procesos en segundo plano:       $ ps -aux
  - Matar procesos:                         $ kill <numero del proceso>
  - Matar procesos stopped o 2o plano:      $ kill -9 <numero del proceso>
  - Ver listado de mensajes del arranque:   $ dmesg
  - Acceder al boot de Linux:               $ mount /dev/mmcblk0p1/ /mnt/
                                            $ cd /mnt
  - Borrar pantalla:                        $ cls
                                            $ clear
  - Acceder al directorio del programa:     $ ve
  - Ver esta ayuda:                         $ ayuda
  - Ver fecha y hora:                       $ date
  - Configurar timezone:                    $ sudo dpkg-reconfigure tzdata
  - Acceder al crontab (planificador de
    aplicaciones programadas)               $ crontab -e
  - Reiniciar la maquina:                   $ reboot
  - Apagar la maquina:                      $ sudo shutdown now
  - Borrar clave SSH para conexiones:       $ ssh-keygen -R <direccion IP>
  - Editar .bashrc:                         $ sudo nano ~/.bashrc
  - Recargar .bashrc sin reboot:            $ . ~/.bashrc
  - Salir de sesion SSH:                    $ exit
  - Version kernel:                         $ uname -r
  - Crear directorio:                       $ mkdir <nombre directorio>
  - Borrar fichero:                         $ rm <nombre fichero>
  - Borrar directorio completo:             $ rm -Rf <nombre directorio>
```
## Licencia:
Copyright 2017 Alfredo Prado Vega
###### @radikalbytes 
http://www.radikalbytes.com
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0
Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.


