import asyncio
import aiohttp
import random
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sys
import signal

class WebStressTester:
    def __init__(self, target_url, num_requests=1000, concurrency=100, use_proxy=False, proxy_file=None):
        self.target_url = target_url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.proxies = []
        self.user_agents = []
        self.stats = {
            'success': 0,
            'failed': 0,
            'total_time': 0,
            'requests_per_second': 0
        }
        self.running = True
        
        # Tải user-agents
        self._load_user_agents()
        
        # Tải proxies nếu được yêu cầu
        if use_proxy and proxy_file:
            self._load_proxies()
        
        # Thiết lập signal handler để dừng chương trình
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def _load_user_agents(self):
        """Tải danh sách user-agents phổ biến"""
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        ]
    
    def _load_proxies(self):
        """Tải danh sách proxy từ file"""
        try:
            with open(self.proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"[INFO] Đã tải {len(self.proxies)} proxies từ {self.proxy_file}")
        except Exception as e:
            print(f"[ERROR] Không thể tải proxies: {e}")
            self.proxies = []
    
    def get_random_user_agent(self):
        """Trả về user-agent ngẫu nhiên"""
        return random.choice(self.user_agents)
    
    def get_random_proxy(self):
        """Trả về proxy ngẫu nhiên"""
        if self.proxies:
            proxy_url = random.choice(self.proxies)
            # Hỗ trợ cả định dạng http và https
            if proxy_url.startswith('http'):
                return proxy_url
            else:
                return f'http://{proxy_url}'
        return None
    
    async def send_request(self, session, request_id):
        """Gửi một request bất đồng bộ"""
        if not self.running:
            return False
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/',
        }
        
        # Thêm các headers ngẫu nhiên để trông tự nhiên hơn
        if random.random() > 0.5:
            headers['DNT'] = '1'
        
        proxy = self.get_random_proxy() if self.use_proxy else None
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with session.get(
                self.target_url, 
                headers=headers, 
                proxy=proxy,
                timeout=timeout,
                ssl=False
            ) as response:
                
                # Đọc nội dung response (tùy chọn)
                if response.status == 200:
                    # await response.text()  # Bỏ comment nếu cần đọc nội dung
                    return True
                else:
                    return False
                    
        except Exception as e:
            # Không hiển thị lỗi để tăng tốc độ
            return False
    
    async def worker(self, session, worker_id, total_requests):
        """Worker xử lý nhiều requests"""
        local_success = 0
        local_failed = 0
        
        for i in range(total_requests):
            if not self.running:
                break
                
            success = await self.send_request(session, i)
            
            if success:
                local_success += 1
            else:
                local_failed += 1
            
            # Cập nhật stats mỗi 100 requests
            if (i + 1) % 100 == 0:
                self.stats['success'] += local_success
                self.stats['failed'] += local_failed
                local_success = 0
                local_failed = 0
        
        # Cập nhật stats còn lại
        self.stats['success'] += local_success
        self.stats['failed'] += local_failed
    
    def print_stats(self, start_time):
        """In thống kê"""
        elapsed_time = time.time() - start_time
        total_requests = self.stats['success'] + self.stats['failed']
        
        if elapsed_time > 0:
            rps = total_requests / elapsed_time
        else:
            rps = 0
        
        sys.stdout.write(
            f"\r[STATS] Thời gian: {elapsed_time:.1f}s | "
            f"Request: {total_requests}/{self.num_requests} | "
            f"Thành công: {self.stats['success']} | "
            f"Thất bại: {self.stats['failed']} | "
            f"RPS: {rps:.1f}       "
        )
        sys.stdout.flush()
    
    async def run_async_test(self):
        """Chạy test bất đồng bộ"""
        print(f"[INFO] Bắt đầu stress test: {self.target_url}")
        print(f"[INFO] Số request: {self.num_requests}, Đồng thời: {self.concurrency}")
        print(f"[INFO] Sử dụng proxy: {self.use_proxy} ({len(self.proxies)} proxies)")
        print("-" * 60)
        
        start_time = time.time()
        
        # Tạo connector với giới hạn cao
        connector = aiohttp.TCPConnector(
            limit=self.concurrency * 2,
            limit_per_host=self.concurrency,
            ttl_dns_cache=300,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        async with aiohttp.ClientSession(
            connector=connector,
            trust_env=True
        ) as session:
            
            # Tính số requests mỗi worker
            requests_per_worker = self.num_requests // self.concurrency
            remaining_requests = self.num_requests % self.concurrency
            
            # Tạo tasks
            tasks = []
            for i in range(self.concurrency):
                worker_requests = requests_per_worker
                if i < remaining_requests:
                    worker_requests += 1
                
                if worker_requests > 0:
                    task = self.worker(session, i, worker_requests)
                    tasks.append(task)
            
            # Chạy tasks và hiển thị tiến trình
            task_group = asyncio.gather(*tasks)
            
            # Hiển thị tiến trình trong khi chạy
            while not task_group.done() and self.running:
                self.print_stats(start_time)
                await asyncio.sleep(0.5)
            
            # Đợi tất cả tasks hoàn thành
            await task_group
        
        # In kết quả cuối cùng
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 60)
        print("[KẾT QUẢ]")
        print(f"URL mục tiêu: {self.target_url}")
        print(f"Tổng thời gian: {elapsed_time:.2f} giây")
        print(f"Tổng số request: {self.stats['success'] + self.stats['failed']}")
        print(f"Request thành công: {self.stats['success']}")
        print(f"Request thất bại: {self.stats['failed']}")
        
        if elapsed_time > 0:
            print(f"Request mỗi giây: {(self.stats['success'] + self.stats['failed']) / elapsed_time:.2f}")
        
        print("=" * 60)
    
    def run(self):
        """Chạy stress test"""
        try:
            # Sử dụng asyncio để chạy test
            asyncio.run(self.run_async_test())
        except KeyboardInterrupt:
            print("\n[INFO] Đã dừng stress test")
        except Exception as e:
            print(f"[ERROR] Lỗi: {e}")
    
    def signal_handler(self, sig, frame):
        """Xử lý signal để dừng chương trình"""
        print("\n[INFO] Đang dừng stress test...")
        self.running = False

def generate_proxy_file(filename, num_proxies=50):
    """Tạo file proxy mẫu (chỉ dành cho mục đích demo)"""
    print(f"[INFO] Tạo file proxy mẫu: {filename}")
    
    # Danh sách proxy mẫu (trong thực tế, bạn cần proxy thật)
    sample_proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://user:pass@proxy3.example.com:8080",
        "https://proxy4.example.com:443",
    ]
    
    # Thêm một số proxy mẫu
    with open(filename, 'w') as f:
        for i in range(min(num_proxies, len(sample_proxies))):
            f.write(sample_proxies[i] + "\n")
        
        # Thêm các proxy giả định
        for i in range(len(sample_proxies), num_proxies):
            port = random.randint(8000, 9000)
            f.write(f"http://proxy{i}.example.com:{port}\n")
    
    print(f"[INFO] Đã tạo {num_proxies} proxies mẫu trong {filename}")
    print("[WARNING] Đây là proxy mẫu, cần thay thế bằng proxy thật để hoạt động!")

def main():
    parser = argparse.ArgumentParser(description='Web Stress Test Tool - Công cụ kiểm tra tải web')
    parser.add_argument('url', help='URL mục tiêu để test')
    parser.add_argument('-n', '--num-requests', type=int, default=1000, 
                       help='Số lượng request (mặc định: 1000)')
    parser.add_argument('-c', '--concurrency', type=int, default=100,
                       help='Số lượng kết nối đồng thời (mặc định: 100)')
    parser.add_argument('-p', '--proxy-file', help='File chứa danh sách proxy (mỗi dòng một proxy)')
    parser.add_argument('--generate-proxies', action='store_true',
                       help='Tạo file proxy mẫu (proxies.txt)')
    
    args = parser.parse_args()
    
    # Tạo file proxy mẫu nếu được yêu cầu
    if args.generate_proxies:
        generate_proxy_file("proxies.txt", 50)
        return
    
    # Kiểm tra và chạy stress test
    use_proxy = bool(args.proxy_file)
    
    tester = WebStressTester(
        target_url=args.url,
        num_requests=args.num_requests,
        concurrency=args.concurrency,
        use_proxy=use_proxy,
        proxy_file=args.proxy_file
    )
    
    tester.run()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║    WEB STRESS TEST TOOL - CỰC MẠNH & NHANH       ║
    ║    Hỗ trợ Proxy & User-Agent Rotation            ║
    ╚══════════════════════════════════════════════════╝
    """)
    main()
