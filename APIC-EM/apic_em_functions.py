import requests
import json
from tabulate import *
from getTicket import getTicket
import urllib3


def getTicket():


    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"

    headers = {

        "Content-Type": "application/json"
    }

    body_json = {

        "password": "Xj3BDqbU",
        "username": "devnetuser"
    }

    resp = requests.post(api_url, json.dumps(body_json), headers = headers, verify = False)

    print("Ticket request status", resp.status_code)

    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"]
    return serviceTicket


def printHosts():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/host"
    ticket = getTicket()
    headers = {
        "Content_type": "application/json",
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url,headers = headers, verify = False)

    print("Status of host request", resp.status_code)

    if resp.status_code != 200:
        raise Exception("El codigo de estado no es 200, algo no ha ido como debía." + resp.text)
        
    response_json = resp.json()


    host_list = []
    i = 0
    for item in response_json["response"]:
        #incrementa el valor de la variable i
        i += 1
        #Obtiene los datos para cada host
        host = [i,item["hostType"],item["hostIp"]]
        host_list.append(host)

    table_header = ["Number", "Type", "IP"]
    print(tabulate(host_list,table_header))
    return host_list

def printDevices():
    api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/network-device"

    ticket = getTicket()
    headers = {
        "Content_type": "application/json",
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url,headers = headers, verify = False)

    print("Status of host request", resp.status_code)

    if resp.status_code != 200:
        raise Exception("El codigo de estado no es 200, algo no ha ido como debía." + resp.text)
        
    response_json = resp.json()


    device_list = []
    i = 0
    for item in response_json["response"]:
        #incrementa el valor de la variable i
        i += 1
        #Obtiene los datos para cada host
        device = [i,item["type"],item["family"],item["role"], item["macAddress"]]
        device_list.append(device)

    table_header = ["Number", "Type","Family", "Role", "MAC"]
    print(tabulate(device_list,table_header))
