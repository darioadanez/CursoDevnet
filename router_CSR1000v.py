#!/usr/bin/env python3
import json
import requests
from tabulate import *
import ncclient
import urllib3
import time
from netmiko import ConnectHandler
from getch import getch
from ncclient import manager
import xml.dom.minidom
import xmltodict

from pprint import pprint


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class router:


    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password= password

    def distintos_modelos(self):
        print("\nInformación del  YANG Cisco-IOS-XE-native:\n")

        m = manager.connect(host=self.host, port=830, username=self.user, password=self.password, hostkey_verify=False)

        netconf_filter = """

            <filter>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
            </filter>
            """

        netconf_reply = m.get_config(source="running", filter = netconf_filter)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        print("Pulse cualquier tecla para ver el siguiente...")
        getch()

        print("\nInformación del modelo YANG ietf-interfaces")

         #Filtro YANG
        netconf_filter = """
            <filter>
                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
            </filter>
            """
        #Realiza la petición
        netconf_reply = m.get(filter=netconf_filter)

        #Convierte a diccionario python la respuesta
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        print("Pulse cualquier tecla para continuar...")
        getch()



    def get_routing(self):
        
        #Realiza la conexión mediante NETCONF
        m = manager.connect(host=self.host, port=830, username=self.user, password=self.password, hostkey_verify=False)

        #Filtro de búsqueda
        netconf_filter = """
            <filter>
                <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
            </filter>
            """
        #Realiza la petición
        netconf_reply = m.get(filter=netconf_filter)
        
        #Deserializa la respuesta
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        #Identificador
        i = 0
        #Lista donde se guardarán las entradas de la tabla
        routing_table = []
        for elem in netconf_reply_dict["rpc-reply"]["data"]["routing-state"]["routing-instance"]["ribs"]["rib"]["routes"]["route"]:
            #Guarda los datos de la ruta
            route = [i, elem["destination-prefix"], elem["next-hop"]["outgoing-interface"]]
            i += 1
            #Añade la ruta a la lista
            routing_table.append(route)

        #Presenta el resultado en formato tabla
        print()
        table_header = ["Identificador", "Red de destino", "Interfaz de salida"]
        print(tabulate(routing_table,table_header))

        print("\nPulse cualquier botón para continuar...")
        getch()


    def get_interfaces(self):

        #Se conecta con netmiko para ejecutar el comando
        sshCli = ConnectHandler(device_type="cisco_ios",host=self.host, port=22,username=self.user,password=self.password)
        output = sshCli.send_command("show ip int brief")
        #Separa la cadena devuelta en lineas. Por cada linea la información de una interfaz
        aux =output.split("\n")
        #Elimina el primer elemento, ya que contiene la cabecera de la tabla
        aux.pop(0)

        interfaces = []

        for i in aux:
            #Separa los diferentes elementos de la interfaz
            y = i.split()
            #Guarda el nombre y la dirección IP
            interface = [y[0], y[1]]
            interfaces.append(interface)

        #Se conecta con netconf para obtener la MAC de cada interfaz
        m = manager.connect(host= self.host, port=830, username= self.user, password= self.password, hostkey_verify=False)
        #Filtro YANG
        netconf_filter = """
            <filter>
                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
            </filter>
            """
        #Realiza la petición
        netconf_reply = m.get(filter=netconf_filter)

        #Convierte a diccionario python la respuesta
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
            #Busca la interfaz con mismo nombre para añadir la dirección MAC
            for i in range(len(interfaces)):
                if interfaces[i][0] == interface["name"]:
                    interfaces[i].append(interface["phys-address"])
                    break
        
        #Presenta el resultado en formato tabla
        print()
        table_header = ["Nombre", "IP Address", "MAC Address"]
        print(tabulate(interfaces,table_header))
        
        print("\nPulse cualquier botón para continuar...")
        getch()


    def delete_interface(self):

        #Solicita el nombre de la interfaz a eliminar

        interface = input("Por favor, introduzca el nombre de la interfaz que desea eliminar: ")


        api_url = "https://" + self.host + "/restconf/data/ietf-interfaces:interfaces/interface=" + interface

        #Cabecera de la aplicación
        headers = {

            "Accept" : "application/yang-data+json",
            "Content-type" : "application/yang-data+json"

        }

        #Autenticación
        basicauth = (self.user, self.password)
        
        resp = requests.delete(api_url,auth = basicauth, headers = headers, verify = False)

       #Muestra el resultado de la operación
        if resp.status_code >= 200 and resp.status_code <= 299:

            print("\nInterfaz eliminada con éxito.")
        else:
            print("\nHa ocurrido un error. Error code: {}, reply: {}".format(resp.status_code,))

        print("\nPulse cualquier botón para continuar...")
        getch()

    def create_interface(self):
        
        #Solicita los parámetros de configuración
        name = input("Introduzca el nombre de la nueva interfaz: ")
        ip = input("Introduzca la IP de la nueva interfaz: ")
        mask = input("Introduzca la máscara de red: ")
        desc = input("Inroduzca una descripción de la interfaz: ")

        #Forma la URL del end-point
        api_url = "https://" + self.host + "/restconf/data/ietf-interfaces:interfaces/interface=" + name

        #Cabecera de la aplicación
        headers = {

            "Accept" : "application/yang-data+json",
            "Content-type" : "application/yang-data+json"

        }

        #Autenticación
        basicauth = (self.user, self.password)

       
        #Configuración de la interfaz 
        yang_config = {

            "ietf-interfaces:interface":
            {
                        "name": name,
                        "description": desc,
                        "type": "iana-if-type:softwareLoopback",
                        "enabled": True,
                        "ietf-ip:ipv4": {
                            "address": [
                                {
                                    "ip": ip,
                                    "netmask": mask
                                }
                            ]
                        },
                        "ietf-ip:ipv6": {}
                    }

        }
        #Utiliza el método put para crear la nueva interfaz
        resp = requests.put(api_url, data = json.dumps(yang_config),  auth = basicauth, headers = headers, verify = False)

        #Muestra el resultado de la operación
        if resp.status_code >= 200 and resp.status_code <= 299:

            print("\nInterfaz creada con éxito.")
        else:
            print("\nHa ocurrido un error. Error code: {}, reply: {}".format(resp.status_code, resp.json()))

        print("\nPulse cualquier botón para continuar...")
        getch()

#Función que es invocada si la opción introducida no coincide con ninguna clave del diccionario#
################################################################################################       
def default():
    print("\n!La opción que ha introducido no es válida!")

###############################################################################################
#Función que muestra un mensaje de despedida y que recoge la opción de salir de la calculadora#
###############################################################################################
def adios():
    print("\n!Adiós! Ha sido un placer.")


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
    opcion = 0 # Inicializa la variable opción, que almacenará la opción elegida por el usuario
     
    dict= {

            1 : router.get_interfaces,
            2 : router.create_interface,
            3 : router.delete_interface,
            4 : router.get_routing,
            5 : router.distintos_modelos,
            6 : adios
           
        }
    #Mientras la opción introducida. Mientras no sea la de salir, sigue en el programa
    while opcion != 6:
        print(
            """
            +=============================================+                            |
            | Seleccione la operación que desee realizar. |
            +=============================================+
            """)
        print("""
            +=============================================+
            | 1.- Ver lista de interfaces                 |
            | 2.- Crear interfaz                          |
            | 3.- Borrar interfaz                         |
            | 4.- Ver tabla de encaminamiento             |
            | 5.- Implementar petición a dos modulos YANG |
            | 6.- Salir de la aplicación                  |
            +=============================================+
            """)
        try:
            opcion = int(input("Opción: "))
        except:
            print("Debe introducir un número entero")
          #Invoca la función que corresponda con la opción introducida
        dict.get(opcion,default)()
    