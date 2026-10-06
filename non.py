#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANONMY SCANER - Port Scanner dengan warna LOLCAT (rainbow berkilau)
Author: Anonymous
"""

import socket
import sys
import time
import os
import threading
from datetime import datetime
from urllib.parse import urlparse

# ==================== KONFIGURASI WARNA ====================
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Rainbow colors
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    PINK = '\033[38;5;213m'
    PURPLE = '\033[38;5;141m'
    
    RAINBOW = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA, PINK, PURPLE]

# ==================== BANNER ASCII ====================
BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⠶⠶⠶⠶⠶⠶⠶⢖⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠞⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡞⠁⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠈⠹⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣼⠋⠀⠀⠀⢀⣤⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⣦⣀⠀⠀⠀⠈⢿⣄⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡾⠁⠀⣠⡾⢁⣾⡿⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⠹⣦⠀⠀⢻⣆⠀⠀⠀⠀
⠀⠀⢀⡾⠁⢀⢰⣿⠃⠾⢋⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⠀⢹⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡌⠻⠆⢿⣧⢀⠀⢻⣆⠀⠀⠀
⠀⠀⣾⠁⢠⡆⢸⡟⣠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣦⡸⣿⠀⣆⠀⢿⡄⠀⠀
⠀⢸⡇⠀⣽⡇⢸⣿⠟⢡⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠙⢿⣿⠀⣿⡀⠘⣿⠀⠀
⡀⣿⠁⠀⣿⡇⠘⣡⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣦⡙⠀⣿⡇⠀⢻⡇⠀
⢸⡟⠀⡄⢻⣧⣾⡿⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣴⣿⠉⡄⢸⣿⠀
⢾⡇⢰⣧⠸⣿⡏⢠⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠀⠓⢶⠶⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⠙⣿⡟⢰⡧⠀⣿⠀
⣸⡇⠰⣿⡆⠹⣠⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣿⡏⠀⠠⢺⠢⠀⠀⣿⣷⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠸⠁⣾⡇⠀⣿⠀
⣿⡇⠀⢻⣷⠀⣿⡿⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⡅⠀⠀⢸⡄⠀⠀⣿⣿⣿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡆⣰⣿⠁⠀⣿⠀
⢸⣧⠀⡈⢿⣷⣿⠃⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣇⠀⢀⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣸⡀⢿⣧⣿⠃⡀⢸⣿⠀
⠀⣿⡀⢷⣄⠹⣿⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⣿⣿⠀⣼⣿⣿⣿⣿⣿⣿⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⢸⡟⢁⣴⠇⣼⡇⠀
⠀⢸⡇⠘⣿⣷⡈⢰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢰⣿⡧⠈⣴⣿⠏⢠⣿⠀⠀
⠀⠀⢿⡄⠘⢿⣿⣦⣿⣯⠘⣆⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⡎⢸⣿⣣⣾⡿⠏⠀⣾⠇⠀⠀
⠀⠀⠈⢷⡀⢦⣌⠛⠿⣿⡀⢿⣆⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣿⡁⣼⡿⠟⣉⣴⠂⣼⠏⠀⠀⠀
⠀⠀⠀⠈⢷⡈⠻⣿⣶⣤⡁⠸⣿⣆⠡⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢀⣾⡟⠀⣡⣴⣾⡿⠁⣴⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢿⣄⠈⢙⠿⢿⣷⣼⣿⣦⠹⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⢡⣾⣿⣶⣿⠿⢛⠉⢀⣾⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣧⡀⠳⣦⣌⣉⣙⠛⠃⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠐⠛⠋⣉⣉⣤⡶⠁⣰⡿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠙⠛⠿⠿⠿⠿⠟⠛⠛⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠙⠟⠛⠿⠿⠿⠿⠟⠛⠁⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢶⣄⠙⠶⣦⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⡶⠖⣁⣴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣶⣄⡉⠉⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠉⠉⠉⠉⣡⣴⡾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⢦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣠⣴⠶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# ==================== FUNGSI WARNA ====================
def rainbow_print(text, delay=0.03, shine=True):
    """Print teks dengan efek rainbow berkilau"""
    colors = Colors.RAINBOW
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(f"{color}{char}{Colors.RESET}")
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    print()

def print_banner():
    """Tampilkan banner dengan efek rainbow berkilau"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    lines = BANNER.strip().split('\n')
    colors = Colors.RAINBOW
    
    # Animasi banner berkilau
    for shine_round in range(2):
        os.system('cls' if os.name == 'nt' else 'clear')
        for line_idx, line in enumerate(lines):
            color = colors[(line_idx + shine_round) % len(colors)]
            print(f"{color}{line}{Colors.RESET}")
        time.sleep(0.25)
    
    # Tampilan final
    os.system('cls' if os.name == 'nt' else 'clear')
    for line_idx, line in enumerate(lines):
        color = colors[line_idx % len(colors)]
        print(f"{color}{line}{Colors.RESET}")
    
    print()
    rainbow_print("        ╔══════════════════════════════════════╗", delay=0.001, shine=False)
    rainbow_print("        ║     ANONMY SCANER - v1.0.0           ║", delay=0.001)
    rainbow_print("        ║     Port Scanner Rainbow Edition     ║", delay=0.001)
    rainbow_print("        ╚══════════════════════════════════════╝", delay=0.001, shine=False)
    print()

def get_target():
    """Ambil input target dari user"""
    print(f"{Colors.CYAN}{Colors.BOLD}[?] Masukkan target URL/IP{Colors.RESET}")
    print(f"{Colors.YELLOW}    Contoh: https://example.com atau 192.168.1.1{Colors.RESET}")
    target = input(f"\n{Colors.GREEN}┌─[{Colors.MAGENTA}ANONMY{Colors.GREEN}]─[{Colors.YELLOW}target{Colors.GREEN}]\n└──╼ {Colors.RESET}$ ").strip()
    
    # Parse URL
    if target.startswith(('http://', 'https://')):
        parsed = urlparse(target)
        host = parsed.hostname
    else:
        host = target.split(':')[0]
    
    return host, target

def scan_port(host, port, timeout=1.0):
    """Scan satu port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_service(port):
    """Deteksi service dari port number"""
    services = {
        20: 'FTP-Data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 67: 'DHCP', 68: 'DHCP', 69: 'TFTP', 80: 'HTTP',
        110: 'POP3', 119: 'NNTP', 123: 'NTP', 135: 'MSRPC', 137: 'NetBIOS',
        138: 'NetBIOS', 139: 'NetBIOS', 143: 'IMAP', 161: 'SNMP', 162: 'SNMP',
        179: 'BGP', 194: 'IRC', 389: 'LDAP', 443: 'HTTPS', 445: 'SMB',
        465: 'SMTPS', 514: 'Syslog', 515: 'LPD', 520: 'RIP', 587: 'SMTP',
        631: 'IPP', 636: 'LDAPS', 873: 'Rsync', 902: 'VMware', 993: 'IMAPS',
        995: 'POP3S', 1080: 'SOCKS', 1194: 'OpenVPN', 1433: 'MSSQL',
        1434: 'MSSQL', 1521: 'Oracle', 1701: 'L2TP', 1723: 'PPTP',
        1883: 'MQTT', 2049: 'NFS', 2082: 'cPanel', 2083: 'cPanel-SSL',
        2181: 'Zookeeper', 2222: 'SSH-Alt', 2375: 'Docker', 2376: 'Docker-SSL',
        3000: 'Node/Grafana', 3128: 'Squid', 3260: 'iSCSI', 3306: 'MySQL',
        3389: 'RDP', 4443: 'HTTPS-Alt', 4444: 'Metasploit', 5000: 'Flask/UPnP',
        5432: 'PostgreSQL', 5555: 'ADB', 5601: 'Kibana', 5672: 'RabbitMQ',
        5900: 'VNC', 5985: 'WinRM', 5986: 'WinRM-SSL', 6379: 'Redis',
        6443: 'K8s-API', 7001: 'WebLogic', 7002: 'WebLogic-SSL',
        8000: 'HTTP-Alt', 8008: 'HTTP-Alt', 8080: 'HTTP-Proxy',
        8081: 'HTTP-Alt', 8086: 'InfluxDB', 8088: 'HTTP-Alt',
        8443: 'HTTPS-Alt', 8888: 'HTTP-Alt', 9000: 'PHP-FPM',
        9090: 'WebSphere', 9092: 'Kafka', 9200: 'Elasticsearch',
        9300: 'Elasticsearch', 9418: 'Git', 9999: 'HTTP-Alt',
        10000: 'Webmin', 11211: 'Memcached', 27017: 'MongoDB',
        27018: 'MongoDB', 50000: 'SAP', 50070: 'Hadoop',
    }
    return services.get(port, 'Unknown')

def scan_ports(host, start_port=1, end_port=1024, threads=100):
    """Scan range port dengan multi-threading"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Memulai scan pada {Colors.YELLOW}{host}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Range port: {Colors.YELLOW}{start_port}-{end_port}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Threads: {Colors.YELLOW}{threads}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Waktu mulai: {Colors.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
    
    open_ports = []
    lock = threading.Lock()
    scanned = [0]
    total = end_port - start_port + 1
    
    def worker(port):
        if scan_port(host, port):
            with lock:
                open_ports.append(port)
                service = get_service(port)
                # Warna berbeda untuk setiap port terbuka
                color = Colors.RAINBOW[port % len(Colors.RAINBOW)]
                print(f"{color}[+] Port {port:<6} OPEN  {Colors.RESET}"
                      f"{Colors.YELLOW}│ {service}{Colors.RESET}")
        with lock:
            scanned[0] += 1
            # Progress bar
            progress = int((scanned[0] / total) * 30)
            bar = f"{Colors.GREEN}{'█' * progress}{Colors.RESET}{'░' * (30 - progress)}"
            sys.stdout.write(f"\r{Colors.CYAN}[{bar}{Colors.CYAN}] {scanned[0]}/{total}{Colors.RESET}")
            sys.stdout.flush()
    
    # Progress animation
    print(f"{Colors.MAGENTA}[~] Scanning...{Colors.RESET}\n")
    
    thread_list = []
    port_queue = list(range(start_port, end_port + 1))
    
    # Batch threading
    for i in range(0, len(port_queue), threads):
        batch = port_queue[i:i+threads]
        threads_batch = []
        for port in batch:
            t = threading.Thread(target=worker, args=(port,))
            t.daemon = True
            t.start()
            threads_batch.append(t)
        for t in threads_batch:
            t.join()
    
    print("\n")
    return open_ports

def display_results(host, open_ports, elapsed):
    """Tampilkan hasil scan"""
    print(f"\n{Colors.CYAN}{'═' * 55}{Colors.RESET}")
    rainbow_print("              📊 HASIL SCAN - ANONMY SCANER", delay=0.002)
    print(f"{Colors.CYAN}{'═' * 55}{Colors.RESET}\n")
    
    print(f"  {Colors.YELLOW}Target     : {Colors.GREEN}{host}{Colors.RESET}")
    print(f"  {Colors.YELLOW}Total Open : {Colors.GREEN}{len(open_ports)} port{Colors.RESET}")
    print(f"  {Colors.YELLOW}Waktu      : {Colors.GREEN}{elapsed:.2f} detik{Colors.RESET}")
    print(f"  {Colors.YELLOW}Timestamp  : {Colors.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
    
    if open_ports:
        print(f"{Colors.MAGENTA}{'─' * 55}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  PORT      STATE    SERVICE{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'─' * 55}{Colors.RESET}")
        for i, port in enumerate(sorted(open_ports)):
            color = Colors.RAINBOW[i % len(Colors.RAINBOW)]
            service = get_service(port)
            print(f"  {color}{port:<9}{Colors.GREEN}OPEN     {Colors.YELLOW}{service}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'─' * 55}{Colors.RESET}")
    else:
        print(f"{Colors.RED}  [!] Tidak ada port terbuka yang ditemukan.{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}{'═' * 55}{Colors.RESET}")
    rainbow_print("         ✨ Scan selesai - ANONMY SCANER ✨", delay=0.003)
    print(f"{Colors.CYAN}{'═' * 55}{Colors.RESET}\n")

def save_results(host, open_ports):
    """Simpan hasil ke file"""
    try:
        filename = f"scan_{host.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write("=" * 55 + "\n")
            f.write("         ANONMY SCANER - SCAN RESULTS\n")
            f.write("=" * 55 + "\n\n")
            f.write(f"Target    : {host}\n")
            f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Open Ports: {len(open_ports)}\n\n")
            f.write("-" * 55 + "\n")
            f.write(f"{'PORT':<10}{'STATE':<10}{'SERVICE'}\n")
            f.write("-" * 55 + "\n")
            for port in sorted(open_ports):
                f.write(f"{port:<10}{'OPEN':<10}{get_service(port)}\n")
            f.write("-" * 55 + "\n")
        print(f"{Colors.GREEN}[✓] Hasil disimpan ke: {Colors.YELLOW}{filename}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[✗] Gagal menyimpan: {e}{Colors.RESET}")

def main():
    try:
        print_banner()
        
        target, raw_target = get_target()
        
        if not target:
            print(f"{Colors.RED}[✗] Target tidak valid!{Colors.RESET}")
            sys.exit(1)
        
        # Resolve hostname
        try:
            ip = socket.gethostbyname(target)
            print(f"\n{Colors.GREEN}[✓] Resolved: {Colors.YELLOW}{target} {Colors.CYAN}→ {Colors.YELLOW}{ip}{Colors.RESET}")
        except socket.gaierror:
            print(f"{Colors.RED}[✗] Tidak bisa resolve hostname: {target}{Colors.RESET}")
            sys.exit(1)
        
        # Pilihan range port
        print(f"\n{Colors.CYAN}Pilih mode scan:{Colors.RESET}")
        print(f"  {Colors.YELLOW}[1]{Colors.RESET} Quick scan (1-1024)")
        print(f"  {Colors.YELLOW}[2]{Colors.RESET} Full scan (1-65535)")
        print(f"  {Colors.YELLOW}[3]{Colors.RESET} Custom range")
        
        choice = input(f"\n{Colors.GREEN}┌─[{Colors.MAGENTA}ANONMY{Colors.GREEN}]─[{Colors.YELLOW}mode{Colors.GREEN}]\n└──╼ {Colors.RESET}$ ").strip()
        
        if choice == '2':
            start_port, end_port, threads = 1, 65535, 200
        elif choice == '3':
            try:
                start_port = int(input(f"{Colors.CYAN}Start port: {Colors.RESET}"))
                end_port = int(input(f"{Colors.CYAN}End port: {Colors.RESET}"))
                threads = int(input(f"{Colors.CYAN}Threads (default 100): {Colors.RESET}") or "100")
            except ValueError:
                print(f"{Colors.RED}[✗] Input tidak valid!{Colors.RESET}")
                sys.exit(1)
        else:
            start_port, end_port, threads = 1, 1024, 100
        
        start_time = time.time()
        open_ports = scan_ports(target, start_port, end_port, threads)
        elapsed = time.time() - start_time
        
        display_results(target, open_ports, elapsed)
        
        # Tanya simpan?
        save = input(f"{Colors.CYAN}Simpan hasil? (y/n): {Colors.RESET}").strip().lower()
        if save == 'y':
            save_results(target, open_ports)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Scan dihentikan oleh user.{Colors.RESET}")
        print(f"{Colors.YELLOW}    Terima kasih telah menggunakan ANONMY SCANER!{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()