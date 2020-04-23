import requests
import json
from tabulate import *
import urllib3
import time

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
            self.timeOut = response_json["response"]["idleTimeout"]

            print("\nSe ha obtenido el ticket con éxito.")
        else:
            print("\nNo ha podido obtenerse el ticket.")

    def print_hosts(self):
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"

        headers = {
            "Content_type": "application/json",
            "X-Auth-Token": self.ticket
        }

        resp = requests.get(api_url,headers = headers, verify = False)

        #print("Status of host request", resp.status_code)

        
        try:
            if resp.status_code != 200:
                raise Exception("El codigo de estado no es 200, algo no ha ido como debía." + resp.text) 

            response_json = resp.json()
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
                raise Exception("El codigo de estado no es 200, algo no ha ido como debía." + resp.text)
                
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

    def get_interfaces(self):
        
        print("\nEsta es la lista de dispositivos de la red: ")
        self.print_devices()
        id = input("\nPor favor, introduzca el identificador del dispositivo que desee conocer sus interfaces (q para salir): ")
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
                raise Exception("El codigo de estado no es 200, algo no ha ido como debía." + resp.text)
                
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

    def get_flow(self):
        #URI del endpoint
        api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/flow-analysis"





        #Muestra la lista de host y de dispositivos encontrados en la red
        #De 10.1.12.20 a 10.1.14.3 funciona
        print("Esta es la lista de host que se ha encontrado:")
        self.print_hosts()


        s_ip = input("Introduzca la dirección IP de origen: ")
        d_ip = input("Introduzca la dirección IP de destino: ")
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
            print("\nEl formato proporcionado de las direcciones IP no es válido")

if __name__ == "__main__":
    apic_em = APIC_EM()
    apic_em.get_ticket()
    #Ver codigos de respuesta de cada petición para porer en los if el caso de que el ticket no sea válido
    #apic_em.print_hosts()
    #apic_em.print_devices()
    #apic_em.get_interfaces()
    apic_em.get_flow()
    #Añadir la de ver la geolocalización de una ip y si acaso la VLAN del los dispositivos
        

