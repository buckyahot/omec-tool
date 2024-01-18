import socket
from scapy.all import conf, srp
from scapy.layers.l2 import ARP, Ether
import subprocess
import requests

import colorama
from colorama import Fore, Style

API_KEY = '474bf9c38698ed'

def print_rainbow_text(text):
    colorama.init()
    rainbow_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        print(color + char, end="")
    print(Style.RESET_ALL)

def scan(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []

    for sent, received in result:
        device_type = get_device_type(received.hwsrc)
        host_name = get_host_name(received.psrc)
        devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'type': device_type, 'host_name': host_name})

    return devices

def get_device_type(mac_address):
    try:
        vendor = mac_address.split(":")[:3]
        vendor_str = ":".join(vendor).upper()

        mobile_vendor_prefixes = ['00:0c:29', '00:1A:2B', '00:25:BC', '00:26:5A', '00:50:F2', '00:A0:C6']
        if any(vendor_str.startswith(prefix) for prefix in mobile_vendor_prefixes):
            return 'Mobile'
    except:
        pass

    return 'Computer'

def get_host_name(ip_address):
    try:
        host_name, _, _ = conf.l3socket.gethostbyaddr(ip_address)
        return host_name
    except:
        return "Unknown"

def get_ip_info(remote_ip):
    try:
        response = requests.get(f'https://ipinfo.io/{remote_ip}?token={API_KEY}')
        data = response.json()

        if response.status_code == 200:
            print("\nInformación de IP para", remote_ip)

            country = data.get('country', 'No disponible')
            region = data.get('region', 'No disponible')
            city = data.get('city', 'No disponible')
            isp = data.get('org', 'No disponible')

            print("Pais:", country)
            print("Region:", region)
            print("Ciudad:", city)
            print("Proveedor de servicios de Internet:", isp)
            print("Latitud / Longitud:", data.get('loc', 'No disponible'))
        else:
            print("\nError al realizar la solicitud. Código de estado:", response.status_code)
            if 'error' in data:
                print("Mensaje de error:", data['error'])
            else:
                print("Respuesta inesperada:", data)

    except requests.exceptions.RequestException as e:
        print("\nError en la solicitud HTTP:", str(e))
    except Exception as e:
        print("\nError:", str(e))

def remote_control():
    server_ip = input("Ingrese la IP del servidor: ")
    server_port = 22 #SSH

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        print("Conexión establecida con el servidor.")

        while True:
            command = input("Ingrese un comando ('exit' para salir): ")
            s.sendall(command.encode('utf-8'))

            if command.lower() == 'exit':
                break

            data = s.recv(1024)
            print(data.decode('utf-8'))

def main():
    ascii_art = """
                                                      
                                                  

                                          ::::::::    :::   :::   :::::::::: :::::::: 
                                        :+:    :+:  :+:+: :+:+:  :+:       :+:    :+: 
                                       +:+    +:+ +:+ +:+:+ +:+ +:+       +:+         
                                      +#+    +:+ +#+  +:+  +#+ +#++:++#  +#+          
                                     +#+    +#+ +#+       +#+ +#+       +#+           
                                    #+#    #+# #+#       #+# #+#       #+#    #+#     
                                    ########  ###       ### ########## ########       
                                                  
                                                  Created by Poetty                                          
                                                           
                                                  
                                         
"""

    print_rainbow_text(ascii_art)

    while True:
        print("\n                                      ╔═══════════════════════════════════════╗")
        print("                                      ║ 1. Escanear dispositivos en la red    ║")
        print("                                      ║ 2. Control remoto                     ║")
        print("                                      ║ 3. Obtener información de IP          ║")
        print("                                      ║ 4. Salir                              ║")
        print("                                      ╠═══════════════════════════════════════╝")
        
        print("                                      ║")
        opcion = input("                                      ╚═══ [?] root : ")

        if opcion == '1':
            print("Escaneando dispositivos en la red...")
        elif opcion == '2':
            print("Iniciando control remoto...")
        elif opcion == '3':
            remote_ip = input("Ingrese la dirección IP a consultar: ")
            get_ip_info(remote_ip)
        elif opcion == '4':
            print("Saliendo del programa. ¡Hasta luego!")
            subprocess.run('cls', shell=True)
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
