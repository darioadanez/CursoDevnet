import requests
import json
from tabulate import *
import urllib3
import time
from getch import getch

class APIC_EM:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.ticket = None
        self.timeOut = None
    #Método que sirve para obtener el ticket de acceso al APIC-EM    
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

        resp = requests.post(api_url, json.dumps(body_json), headers = headers, verify = False)

        if (resp.status_code == 200) or (resp.status_code == 200):

            response_json = resp.json()
            self.ticket = response_json["response"]["serviceTicket"]
            #self.timeOut = response_json["response"]["idleTimeout"]

            print("\nSe ha obtenido el ticket con éxito.\nSu ticket es:", self.ticket)
        else:
            print("\nNo ha podido obtenerse el ticket.")
        print("\nPulse cualquier tecla para continuar...")
        getch()

    def print_hosts(self):
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"

        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)

        #print("Status of host request", resp.status_code)

        response_json= resp.json()
        try:
            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
            host_list = []
            i = 0
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                i += 1
                #Obtiene los datos para cada host
                host = [i,item["hostType"], item["hostMac"],item["hostIp"], item["connectedNetworkDeviceIpAddress"]]
                host_list.append(host)

            table_header = ["Número", "Tipo", "MAC" ,"IP", "IP dispositivo conectado"]
            print(tabulate(host_list,table_header))
            #return host_list
        except Exception as err:
            print("No ha sido posible obtener el listado de los host de la red.\n", err)

        print("Pulse cualquier tecla para continuar...")
        getch()

    def print_devices(self):

        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device"

        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)

        print("Status of host request", resp.status_code)
        try:

            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
                
            response_json = resp.json()


            device_list = []
            i = 0
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                i += 1
                #Obtiene los datos para cada host
                device = [i,item["type"],item["family"],item["role"], item["macAddress"], item["id"]]
                device_list.append(device)

            table_header = ["Número", "Tipo","Familia", "Rol", "MAC", "ID"]
            print(tabulate(device_list,table_header))
        except Exception as err:
            print("No ha sido posible obtener el listado de los host de la red.\n", err)

        print("\nPulse cualquier tecla para continuar...")
        getch()

    def get_interfaces(self):
        
        print("\nEsta es la lista de dispositivos de la red: ")
        self.print_devices()
        id = input("\nPor favor, introduzca el identificador del dispositivo que desee conocer sus interfaces (q para salir): ").strip()
        if id == 'q':
            return

        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/interface"
        #print("Status of host request", resp.status_code)
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)
        print("Status of host request", resp.status_code)
        try:

            if resp.status_code != 200:
                print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
                return
                
            response_json = resp.json()


            interface_list = []
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                if item["deviceId"] == id:
                   
                    #Obtiene los datos para cada host
                    interface = [item["ifIndex"],item["interfaceType"],item["status"],item["ipv4Address"], item["macAddress"], item["portName"]]
                    interface_list.append(interface)
            table_header = ["Número", "Tipo","Estado", "IP", "MAC", "Nombre"]
            print(tabulate(interface_list,table_header))
        except Exception as err:
            print ("No ha sido posible obtener las interfaces del dispositivo.")
        
        print("\nPulse cualquier tecla para continuar...")
        getch()

    def get_flow(self):
        #URI del endpoint
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/flow-analysis"





        #Muestra la lista de host y de dispositivos encontrados en la red
        #De 10.1.12.20 a 10.1.14.3 funciona
        print("Esta es la lista de host que se ha encontrado:")
        self.print_hosts()


        s_ip = input("Introduzca la dirección IP de origen (q para salir): ").strip()
        d_ip = input("Introduzca la dirección IP de destino (q para salir): ").strip()
        if s_ip == 'q' or d_ip == 'q':
            return
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": self.ticket
        }
        body = {
        
        "destIP": d_ip,
        "sourceIP": s_ip
        
        }

        resp = requests.post(api_url, json.dumps(body), headers = headers, verify = False)
        tiempo_inicial = time.time()
        resp_json = resp.json()
        print(resp.status_code)
        if resp.status_code == 202 or resp.status_code == 200:

            flowAnalysisId = resp_json["response"]["flowAnalysisId"]

            #Realiza la operación GET para obtener el resultado
            api_url = api_url + "/" + str(flowAnalysisId)
            while (True):

                resp = requests.get(api_url, headers = headers, verify = False)

                resp_json = resp.json()
                #print(resp_json)
                if resp_json["response"]["request"]["status"] == "FAILED":
                    print("Algo ha ido mal con la petición")
                    print(resp_json["response"]["request"]["failureReason"])
                    break
                elif resp_json["response"]["request"]["status"] == "INPROGRESS":
                    if (time.time() - tiempo_inicial) >= 60:
                        print("Ha expirado el tiempo máximo, parece que la ruta no puede ser calculada.")
                        resp = requests.delete(api_url, headers = headers, verify = False)
                        break
                    print("Espere por favor...")
                elif resp_json["response"]["request"]["status"] == "COMPLETED":
                    i = 0
                    list_items = []
                    for item in resp_json["response"]["networkElementsInfo"]:
                        i += 1
                        elem = [i]
                        try:
                            elem.append(item["ip"])
                        except:
                            elem.append("Desconocida")
                        try:
                            elem.append(item["type"])
                        except:
                            elem.append("Desconocido")

                        list_items.append(elem)
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

    def muestra_vlan(self):

        print("\nEsta es la lista de dispositivos de la red: ")
        self.print_devices()

        id = input("\nPor favor, introduzca el identificador del dispositivo del que desee obtener sus redes (q para salir): ").strip()
        if id == 'q':
            return

        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device" + "/" + id + "/vlan"
        #print("Status of host request", resp.status_code)
        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)
        #print("Status of host request", resp.status_code)
        
        if resp.status_code != 200:
           print("El codigo de estado no es 200, algo no ha ido como debía.",eval(resp.text)["response"]["detail"], sep="\n")
           return
            
        response_json = resp.json()
        


        vlan_list = []
        i = 0
        for item in response_json["response"]:
            
            vlan= []
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
        table_header = ["VID", "IP","Nombre interfaz"]
        print(tabulate(vlan_list,table_header))

        print("\nPulse cualquier tecla para continuar...")
        getch()

    def localiza_IP(self):

        ip = input("Por favor, intriduzca la dirección IP que desea geolocalizar (q para salir): ").strip()

        if ip == 'q':
            return
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ipgeo/" + ip

        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)
        if resp.status_code != 200:
           print("La petición no ha podido ser llevada a cabo",eval(resp.text)["response"]["detail"], sep="\n")
           return
            
        response_json = resp.json()
       
        item = response_json["response"][ip]
            
        localizacion = [[item["city"], item["subDivision"], item["country"], item["continent"], item["latitude"], item["longitude"]], ]

        table_header = ["Ciudad", "Subdivisión", "País", "Continente", "Latitud", "Longitud"]
        
        print()
        print(tabulate(localizacion,table_header))

        print("\nPulse cualquier tecla para continuar...")
        getch()
        
def default():
    print("\n!La opción que ha introducido no es válida!")
def adios():
    print("!Adiós! Ha sido un placer.")
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
        
        dict.get(opcion,default)()

if __name__ == "__main__":
    main()
   
        

