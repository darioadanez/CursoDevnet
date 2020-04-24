import requests
import json
from tabulate import *
import urllib3
import time
from getch import getch

#Clase que contiene las operaciones a realizar en el APIC-EM
class APIC_EM:

    ##########################################################################################################
    #Método que inicializa los atributos del objeto. Es invocado cuando se crea un objeto de la clase APIC_EM#
    ##########################################################################################################
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.ticket = None
        #self.timeOut = None
     
    ##############################################################
    #Método que sirve para obtener el ticket de acceso al APIC-EM#
    ##############################################################    
    def get_ticket(self):

        #URL del end-point
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"

        #Cabecera de la petición
        headers = {

            "Content-Type": "application/json"
        }
        #Cuerpo de la petición
        body_json = {

            "password": "Xj3BDqbU",
            "username": "devnetuser"
        }

        #Utiliza el método POST para solicitar el ticket
        resp = requests.post(api_url, json.dumps(body_json), headers = headers, verify = False)

        #Si el codigo de estado devuelto es 200 o 202 significa que la petición se ha realizado con éxito
        if (resp.status_code == 200) or (resp.status_code == 200):
            
            #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python
            response_json = resp.json()
            self.ticket = response_json["response"]["serviceTicket"]
            #self.timeOut = response_json["response"]["idleTimeout"]

            print("\nSe ha obtenido el ticket con éxito.\nSu ticket es:", self.ticket)
        #Si no es así, informa del error
        else:
            print("\nNo ha podido obtenerse el ticket.")
        print("\nPulse cualquier tecla para continuar...")
        getch()

    ##################################################
    #Método que muestra la lista de hosts del sistema#
    ##################################################
    def print_hosts(self):
        
        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return
        #URL del endpoint
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"

        #Cabeceras de la petición
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        #Utiliza el método GET para realizar la peitición
        resp = requests.get(api_url,headers = headers, verify = False)

        #print("Status of host request", resp.status_code)
        
        try:
            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
            #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python
            response_json= resp.json()
            host_list = []
            i = 0
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                i += 1
                #Obtiene los datos para cada host
                host = [i,item["hostType"], item["hostMac"],item["hostIp"], item["connectedNetworkDeviceIpAddress"]]
                host_list.append(host)
            #Cabecera de la tabla
            table_header = ["Número", "Tipo", "MAC" ,"IP", "IP dispositivo conectado"]
            print(tabulate(host_list,table_header))
            #return host_list
        except Exception as err:
            print("No ha sido posible obtener el listado de los host de la red.\n", err)

        print("Pulse cualquier tecla para continuar...")
        getch()
    
    ###############################################
    #Método que muestra los dispositivos de la red#
    ###############################################
    def print_devices(self):
        
        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return
        #URL del end-point
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device"

        #Cabecera de la petición
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }
        #Utiliza el método GET para realizar la petición
        resp = requests.get(api_url,headers = headers, verify = False)

        #print("Status of host request", resp.status_code)
        try:
            #Comprueba si la petición ha sido exitosa
            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
            #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python   
            response_json = resp.json()

            #Inicializa las variables
            device_list = []
            i = 0
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                i += 1
                #Obtiene los datos para cada host
                device = [i,item["type"],item["family"],item["role"], item["macAddress"], item["id"]]
                device_list.append(device)
            #Cabecera de la tabla
            table_header = ["Número", "Tipo","Familia", "Rol", "MAC", "ID"]
            print()
            print(tabulate(device_list,table_header))
        except Exception as err:
            print("No ha sido posible obtener el listado de los host de la red.\n", err)

        print("\nPulse cualquier tecla para continuar...")
        getch()

    ################################################################################
    #Método que solicita el identificador de un dipositivo y muestra sus interfaces#
    ################################################################################
    def get_interfaces(self):

        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return
        #Muestra los dispositivos de la red
        print("\nEsta es la lista de dispositivos de la red: ")
        self.print_devices()

        #Solicita el identificador del dispositivo que se deseen conocer sus interfaces
        id = input("\nPor favor, introduzca el identificador del dispositivo que desee conocer sus interfaces (q para salir): ").strip()
        if id == 'q':
            return
        #URL del end-point
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/interface"
        #print("Status of host request", resp.status_code)

        #Cabecera de la petición
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        #Utiliza el método GET para realizar la petición
        resp = requests.get(api_url,headers = headers, verify = False)
        
        try:
            
            #Si el estado de la cosulta no es 200, muestra que ha habido un error
            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
            #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python    
            response_json = resp.json()


            interface_list = []
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                if item["deviceId"] == id:
                   
                    #Obtiene los datos para cada host
                    interface = [item["ifIndex"],item["interfaceType"],item["status"],item["ipv4Address"], item["macAddress"], item["portName"]]
                    interface_list.append(interface)
            #Cabecera de la tabla
            table_header = ["Número", "Tipo","Estado", "IP", "MAC", "Nombre"]
            print()
            print(tabulate(interface_list,table_header))
        except Exception as err:
            print ("No ha sido posible obtener las interfaces del dispositivo.")
        
        print("\nPulse cualquier tecla para continuar...")
        getch()
    ###########################################
    #Método que muestra la ruta entre dos host#
    ###########################################
    def get_flow(self):

        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return

        #URI del endpoint
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/flow-analysis"

        #Muestra la lista de host y de dispositivos encontrados en la red
        #De 10.1.12.20 a 10.1.14.3 funciona. Con otras combinaciones también, pero hay algunas que no es capaz de obtener la ruta
        print("Esta es la lista de host que se ha encontrado:")
        self.print_hosts()
        
        #Solicita las direcciones IP
        s_ip = input("Introduzca la dirección IP de origen (q para salir): ").strip()
        d_ip = input("Introduzca la dirección IP de destino (q para salir): ").strip()
        if s_ip == 'q' or d_ip == 'q':
            return
        #Cabecera de la peticion
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": self.ticket
        }
        #Cuerpo de la petición
        body = {
        
        "destIP": d_ip,
        "sourceIP": s_ip
        
        }
        #Utiliza el método POST para crear la solicitud
        resp = requests.post(api_url, json.dumps(body), headers = headers, verify = False)
        #Comienza a contar el tiempo de procesado de la petición
        tiempo_inicial = time.time()
        #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python
        resp_json = resp.json()

        #Si el codigo de respuesta no es 200 o 202, muestra un mensaje de error
        if resp.status_code == 202 or resp.status_code == 200:
            
            #Obtiene el identificador del flujo
            flowAnalysisId = resp_json["response"]["flowAnalysisId"]

            #Realiza la operación GET para obtener el resultado
            api_url = api_url + "/" + str(flowAnalysisId) #Añade el ID para consultar los resultados
            while (True):
                #Utiliza el método post para obtener los resultados
                resp = requests.get(api_url, headers = headers, verify = False)
                #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python
                resp_json = resp.json()
                
                #El estadp FAILED siginifica que el flujo no ha podido ser calculado
                if resp_json["response"]["request"]["status"] == "FAILED":
                    print("Algo ha ido mal con la petición")
                    print(resp_json["response"]["request"]["failureReason"])
                    break
                #Significa que aún está calculando la ruta
                elif resp_json["response"]["request"]["status"] == "INPROGRESS":
                    #Si tarda más de un mínuto en estar disponible, se da por imposible y se borra la solicitud
                    if (time.time() - tiempo_inicial) >= 60:
                        print("Ha expirado el tiempo máximo, parece que la ruta no puede ser calculada.")
                        resp = requests.delete(api_url, headers = headers, verify = False)
                        break
                    print("Espere por favor...")
                #Significa que se ha obtenido la ruta con éxito
                elif resp_json["response"]["request"]["status"] == "COMPLETED":
                    i = 0
                    list_items = []
                    #Itera sobre el resultado
                    for item in resp_json["response"]["networkElementsInfo"]:
                        i += 1
                        elem = [i]
                        #Añade IP
                        try:
                            elem.append(item["ip"])
                        except:
                            elem.append("Desconocida")
                        #Añade tipo
                        try:
                            elem.append(item["type"])
                        except:
                            elem.append("Desconocido")

                        list_items.append(elem)
                    #Cabecera de la petición
                    table_header = ["Número", "IP", "Tipo"]
                    print(tabulate(list_items,table_header))
                    break
                    #Espera dos segundos para no mandar peticiones constantemente
                time.sleep(2)
        else: 
            print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
            return

        print("\nPulse cualquier tecla para continuar...")
        getch()

    #########################################################
    #Método que muestra las VLAN presentes en un dispositivo#
    #########################################################
    def muestra_vlan(self):

        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return

        #Muestra la lista de dispositivos de red
        print("\nEsta es la lista de dispositivos de la red: ")
        self.print_devices()

        #Solicita el identificador de dispositivo
        id = input("\nPor favor, introduzca el identificador del dispositivo del que desee obtener sus redes (q para salir): ").strip()
        if id == 'q':
            return

        #URL del ENPOINT
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device" + "/" + id + "/vlan"
        #Cabecera de la petición
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        #Utiliza el método GET para realizar la petición
        resp = requests.get(api_url,headers = headers, verify = False)

        #Si el código de estado no es 200, informa del error        
        if resp.status_code != 200:
           print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
           return
        #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python    
        response_json = resp.json()
        
        vlan_list = []
        i = 0
        #Itera sobre el resultado
        for item in response_json["response"]:
            
            vlan= []
            #Utiliza try-excep porque no en todos los elementos vienen los mismos campos y puede generar errores
            try:
                vlan.append(item["vlanNumber"])
            except:
                vlan.append("Desconocido")
            try:
                vlan.append(item["ipAddress"])
            except:
                vlan.append("Desconocida")
            try:
                vlan.append(item["interfaceName"])
            except:
                vlan.append("Desconocido")
            vlan_list.append(vlan)
        #Cabecera de la petición
        table_header = ["VID", "IP","Nombre interfaz"]
        print()
        print(tabulate(vlan_list,table_header))

        print("\nPulse cualquier tecla para continuar...")
        getch()

    ########################################################################
    #Método que solicita una IP y muestra información sobre su localización#
    ########################################################################
    def localiza_IP(self):
        
        #Comprueba que hay un ticket solicitado
        if self.ticket == None:
            print("\nPrimero debe obtener su ticket.\n")
            return

        #Solicita la dirección IP
        ip = input("Por favor, intriduzca la dirección IP que desea geolocalizar (q para salir): ").strip()

        if ip == 'q':
            return
        #URL del end-point
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ipgeo/" + ip
        #Cabecera de la petición
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        #Utiliza el método get para realizar la consulta
        resp = requests.get(api_url,headers = headers, verify = False)
        #Muestra mensaje de error si el codigo no es 200
        if resp.status_code != 200:
           print("La petición no ha podido ser llevada a cabo",eval(resp.text)["response"]["detail"], sep="\n")
           return
        
        #Deserializa la respuesta en formato json para trabajar con los datos en formato de diccionario Python
        response_json = resp.json()
        
        item = response_json["response"][ip]
        #Guarda los datos más relevantes
        localizacion = [[item["city"], item["subDivision"], item["country"], item["continent"], item["latitude"], item["longitude"]], ]
        #Cabecera de la petixión
        table_header = ["Ciudad", "Subdivisión", "País", "Continente", "Latitud", "Longitud"]
        #Muestra resultado
        print()
        print(tabulate(localizacion,table_header))

        print("\nPulse cualquier tecla para continuar...")
        getch()

################################################################################################
#Función que es invocada si la opción introducida no coincide con ninguna clave del diccionario#
################################################################################################       
def default():
    print("\n!La opción que ha introducido no es válida!")

###############################################################################################
#Función que muestra un mensaje de despedida y que recoge la opción de salir de la calculadora#
###############################################################################################
def adios():
    print("!Adiós! Ha sido un placer.")

##############
#Función main#
##############
def main ():

    apic_em = APIC_EM()
    opcion = 0 # Inicializa la variable opción, que almacenará la opción elegida por el usuario
    #Crea un diccionario para emular la estructura switch-case de otros lenguajes de programación
    dict= {

            1 : apic_em.get_ticket,
            2 : apic_em.print_hosts,
            3 : apic_em.print_devices,
            4 : apic_em.get_interfaces,
            5 : apic_em.muestra_vlan,
            6 : apic_em.get_flow,
            7 : apic_em.localiza_IP, 
            8 : adios
        }
    #Mientras la opción introducida. Mientras no sea la de salir, sigue en el programa
    while opcion != 8:
        print(
            """
            +=============================================+
            | ¡Bienvenido a la aplicación para interctuar |
            | con el APIC-EM!                             |
            | Seleccione la operación que desee realizar. |
            +=============================================+
            """)
        print("""
            +=============================================+
            | 1.- Obtener ticket de acceso                |
            | 2.- Ver host de la red                      |
            | 3.- Ver dispositivos de la red              |
            | 4.- Ver interfaces de un dispositivo        |
            | 5.- Ver VLAN de un dispositivo              |
            | 6.- Ver flujo entre dos host                |
            | 7.- Ver geolocalización de una IP           |
            | 8.- Salir de la aplicación                  |
            +=============================================+
            """)
        try:
            opcion = int(input("Opción: "))
        except:
            print("Debe introducir un número entero")
          #Invoca la función que corresponda con la opción introducida
        dict.get(opcion,default)()

if __name__ == "__main__":
    main()
   
        

