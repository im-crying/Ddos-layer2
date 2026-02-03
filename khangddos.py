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
            'user', 'profile', 'account', 'login', 'register
