from scapy.all import *
import random
import time

# Tabelas NAT para os dois roteadores (Port Address Translation - PAT)
nat_table_r1 = {}
nat_table_r2 = {}

# IPs e portas de exemplo
router1_internal_ip = "192.168.1.1"
router1_external_ip = "10.10.10.1"
router2_internal_ip = "192.168.2.1"
router2_external_ip = "20.20.20.1"

# IPs na rede privada 1 (192.168.1.2 - 192.168.1.6)
network1_ips = [f"192.168.1.{i}" for i in range(2, 7)]

# IPs na rede privada 2 (192.168.2.2)
network2_ips = [f"192.168.2.{i}" for i in range(2, 7)]

# Lista para armazenar pacotes processados
packets_log = []

# Função para simular o envio de um pacote de uma rede privada para a outra
def send_packet(src_ip, dst_ip, src_port, dst_port):
    packet = IP(src=src_ip, dst=dst_ip)/TCP(sport=src_port, dport=dst_port)
    return packet

# Função para realizar o NAT no roteador 1
def apply_nat_r1(packet):
    global nat_table_r1

    if packet[IP].src.startswith("192.168.1."):
        if (router1_external_ip, packet[TCP].sport) in nat_table_r1:
            packet[IP].src, packet[TCP].sport = nat_table_r1[(router1_external_ip, packet[TCP].sport)]
        else:
            nat_port = random.randint(10000, 60000)
            nat_table_r1[(router1_external_ip, packet[TCP].sport)] = (packet[IP].src, nat_port)
            packet[IP].src, packet[TCP].sport = router1_external_ip, nat_port
    else:
        if (packet[IP].dst, packet[TCP].dport) in nat_table_r1:
            packet[IP].dst, packet[TCP].dport = nat_table_r1[(packet[IP].dst, packet[TCP].dport)]
        else:
            return packet

    packets_log.append(packet)
    return packet

# Função para realizar o NAT no roteador 2
def apply_nat_r2(packet):
    global nat_table_r2

    if packet[IP].src.startswith("192.168.2."):
        if (router2_external_ip, packet[TCP].sport) in nat_table_r2:
            packet[IP].src, packet[TCP].sport = nat_table_r2[(router2_external_ip, packet[TCP].sport)]
        else:
            nat_port = random.randint(10000, 60000)
            nat_table_r2[(router2_external_ip, packet[TCP].sport)] = (packet[IP].src, nat_port)
            packet[IP].src, packet[TCP].sport = router2_external_ip, nat_port
    else:
        if (packet[IP].dst, packet[TCP].dport) in nat_table_r2:
            packet[IP].dst, packet[TCP].dport = nat_table_r2[(packet[IP].dst, packet[TCP].dport)]
        else:
            return packet

    packets_log.append(packet)
    return packet

# Função para simular tráfego entre as duas redes privadas
def simulate_traffic():
    while True:
        for src_ip in network1_ips:
            for dst_ip in network2_ips:
                src_port = random.randint(10000, 60000)
                dst_port = 80

                packet = send_packet(src_ip, dst_ip, src_port, dst_port)
                nat_packet1 = apply_nat_r1(packet)
                nat_packet2 = apply_nat_r2(nat_packet1)
                packets_log.append(nat_packet2)

                return_packet = send_packet(dst_ip, src_ip, dst_port, src_port)
                nat_return_packet1 = apply_nat_r2(return_packet)
                original_packet = apply_nat_r1(nat_return_packet1)
                packets_log.append(original_packet)

        # Pausa entre envios de pacotes para simular tráfego contínuo
        time.sleep(1)

# Função para obter os pacotes processados
def get_packets_log():
    formatted_log = []
    seen_pairs = set()

    for packet in packets_log:
        # Verifica se o pacote veio da rede privada 1
        if packet[IP].src.startswith("192.168.1."):
            global_entry = f"{router1_external_ip}:{packet[TCP].sport}"
            local_entry = f"{packet[IP].src}:{packet[TCP].sport}"
            global_exit = f"{router2_external_ip}:{packet[TCP].dport}"
            local_exit = f"{packet[IP].dst}:{packet[TCP].dport}"
        # Verifica se o pacote veio da rede privada 2
        elif packet[IP].src.startswith("192.168.2."):
            global_entry = f"{router2_external_ip}:{packet[TCP].sport}"
            local_entry = f"{packet[IP].src}:{packet[TCP].sport}"
            global_exit = f"{router1_external_ip}:{packet[TCP].dport}"
            local_exit = f"{packet[IP].dst}:{packet[TCP].dport}"
        else:
            continue  # Se não for de nenhuma rede privada, ignora o pacote

        # Verifica se já registrou essa combinação de IPs
        entry_tuple = (global_entry, local_entry)
        exit_tuple = (global_exit, local_exit)
        if (entry_tuple, exit_tuple) in seen_pairs:
            continue
        seen_pairs.add((entry_tuple, exit_tuple))

        # Adiciona ao log formatado
        formatted_log.append((global_entry, local_entry, global_exit, local_exit))

    return formatted_log
