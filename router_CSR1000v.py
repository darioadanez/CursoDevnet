#!/usr/bin/env python3
import json
import requests
import tabulate
import ncclient
import urllib3
import time
from netmiko import ConnectHandler


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class router:


    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password= password

    def create_interface(self):
        
        #Solicita los diferentes parámetros que definen la interfaz
        while True:
            
            #Pide el tipo de interfaz y comprueba que se h introducido una opción correcta
            tipo = int(input("\nIntroduzca 1 si desea crear una interfaz GigabitEthernet y 2 si desea crear una interfaz de Loopback: "))
            
            if tipo != 1 or tipo != 2:
                print("\nPor favor, introduzca una de las dos opciones permitidas: ")
            else:
                break
        #Solicita el resto de parámetros
        name = input("Introduzca el nombre de la nueva interfaz: ")
        ip = input("Introduzca la IP de la nueva interfaz: ")
        mask = input("Introduzca la máscara de red: ")
        desc = input("Inroduzca una descripción de la interfaz: ")

        #Forma la URL del end-point
        api_url = "https://" + self.host + "restconf/data/ietf-interfaces:interfaces/interface=" + name

        #Cabecera de la aplicación
        headers = {

            "Accept" : "application/yang-data+json",
            "Content-type" : "application/yang-data+json"

        }

        basicauth = (self.user, self.password)


if __name__ == "__main__":
    
    ip = input("Introduzca la IP del router: ")
    user = input("Introduzca el login: ")
    password = input("Introduzca la contraseña de acceso al router: ")

    try:

        sshCli = ConnectHandler(device_type="cisco_ios",host=ip, port=22,username=user,password=password)
        sshCli.disconnect()
    except Exception as err:
        print("No se ha podido conectar al router, revise los datos introducidos\n", err)
        exit()
    
    router = router(ip,user,password)


    