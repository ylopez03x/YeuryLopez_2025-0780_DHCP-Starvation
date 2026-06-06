# DHCP Starvation Attack
**Autor:** Yeury Lopez de Leon  
**Matrícula:** 2025-0780  
**Materia:** Seguridad de Redes  
**Fecha:** 31/05/2026  

[Ver demostración en YouTube](https://youtu.be/NvZqfwklTWI)
---

## Objetivo del Laboratorio
Demostrar el ataque DHCP Starvation en un entorno controlado, 
evidenciando cómo un atacante puede agotar el pool de direcciones 
IP del servidor DHCP legítimo, impidiendo que nuevos clientes 
obtengan configuración de red.

---

## Objetivo del Script
Enviar miles de solicitudes DHCP Discover con MACs falsas para 
agotar completamente el pool de IPs del servidor DHCP (R1).

### Parámetros usados
| Parámetro | Valor | Descripción |
|---|---|---|
| INTERFAZ | eth0 | Interfaz de Kali hacia SW1 |
| PAQUETES | 60 | Cantidad de solicitudes DHCP falsas |
| Pool objetivo | 172.25.78.50-100 | Rango DHCP de R1 |
| INTERVALO | 0.1 seg | Pausa entre paquetes |

### Requisitos para utilizar la herramienta
- Kali Linux con Python 3
- Librería Scapy instalada
- Permisos root
- Conectividad con el servidor DHCP objetivo

---

## Documentación del funcionamiento del Script

**1. Generación de MACs falsas**  
La función `random_mac()` genera MACs completamente aleatorias 
para cada solicitud DHCP simulando clientes diferentes.

**2. Generación de hostnames falsos**  
La función `random_hostname()` genera nombres de host falsos 
como laptop-123, desktop-456, phone-789.

**3. Construcción del DHCP Discover**  
Cada paquete contiene una capa Ethernet, IP, UDP y BOOTP con 
la MAC falsa en el campo chaddr, simulando un cliente real.

**4. Agotamiento del pool**  
R1 asigna una IP a cada MAC falsa hasta que no quedan IPs 
disponibles en el pool 172.25.78.50-100.

---

## Documentación de la Red

### Topología
> <img width="705" height="617" alt="image" src="https://github.com/user-attachments/assets/08a15efd-a611-4c3e-98b3-eaf35f21f5ab" />


### Direccionamiento IP
| Dispositivo | Interfaz | Dirección IP | Máscara | Rol |
|---|---|---|---|---|
| R1 | fa0/0 | 172.25.78.1 | /24 | Gateway + DHCP Server |
| SW1 | VLAN1 | 172.25.78.2 | /24 | Switch Core - Root Bridge |
| SW2 | VLAN1 | 172.25.78.3 | /24 | Switch Acceso |
| Kali | eth0 | 172.25.78.10 | /24 | Atacante |
| PC1 | eth0 | 172.25.78.20 | /24 | Víctima 1 (estática) |
| PC2 | eth0 | 172.25.78.21 | /24 | Víctima 2 (DHCP) |

### Conexiones
| Dispositivo A | Interfaz | Dispositivo B | Interfaz |
|---|---|---|---|
| R1 | fa0/0 | SW1 | e0/0 |
| SW1 | e0/1 | Kali | eth0 |
| SW1 | e0/2 | PC1 | eth0 |
| SW1 | e0/3 | SW2 | e0/0 |
| SW2 | e0/1 | PC2 | eth0 |

### Herramientas utilizadas
- EVE-NG Community Edition
- Cisco IOL L2 v15.1 (SW1, SW2)
- Cisco IOS 3725 v12.4 Dynamips (R1)
- Kali Linux 2024
- Python 3 + Scapy
- VPCS (PC1, PC2)

---

## Capturas de Pantalla

### Pool DHCP antes del ataque
> <img width="933" height="286" alt="image" src="https://github.com/user-attachments/assets/f0d3e1c4-5016-4df9-a934-42912c36c4d8" />


### Ejecución del script
> <img width="936" height="723" alt="image" src="https://github.com/user-attachments/assets/292afacf-11ac-44c1-8257-1091a65dca53" />


### Pool DHCP agotado
> <img width="944" height="388" alt="image" src="https://github.com/user-attachments/assets/18240f8a-a149-49ac-8d3b-266520bd65a3" />


### PC2 sin poder obtener IP
> <img width="967" height="611" alt="image" src="https://github.com/user-attachments/assets/0fca875d-752b-46a8-a3ab-50c3f3dc18d3" />


---

## Contramedidas

### DHCP Snooping en SW1
```cisco
ip dhcp snooping
ip dhcp snooping vlan 1
interface ethernet 0/0
 ip dhcp snooping trust
interface ethernet 0/1
 ip dhcp snooping limit rate 10
```

### Resultado
DHCP Snooping limita la cantidad de solicitudes DHCP por puerto, 
bloqueando el ataque de agotamiento.
