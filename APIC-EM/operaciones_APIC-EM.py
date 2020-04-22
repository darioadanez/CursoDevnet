import requests
import json
from tabulate import *
import urllib3

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
                host = [i,item["hostType"], item["hostMac"],item["hostIp"]]
                host_list.append(host)

            table_header = ["Número", "Tipo", "MAC" ,"IP"]
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
        
        id = input("Por favor, introduzca el identificador del dispositivo que desee conocer sus interfaces (q para salir): ")
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
            i = 0
            for item in response_json["response"]:
                #incrementa el valor de la variable i
                if item["deviceId"] == id:
                    i += 1
                    #Obtiene los datos para cada host
                    interface = [i,item["interfaceType"],item["status"],item["ipv4Address"], item["macAddress"], item["portName"]]
                    interface_list.append(interface)
            table_header = ["Número", "Tipo","Estado", "IP", "MAC", "Nombre"]
            print(tabulate(interface_list,table_header))
        except Exception as err:
            print ("No ha sido posible obtener las interfaces del dispositivo.")


if __name__ == "__main__":
    apic_em = APIC_EM()
    apic_em.get_ticket()
    #apic_em.print_hosts()
    #apic_em.print_devices()
    apic_em.get_interfaces()
        

