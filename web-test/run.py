#!/usr/bin/env python3
import sys
import os

# Thêm thư mục hiện tại vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from stress_test import AdvancedWebStressTester
    
    # CẤU HÌNH TEST - THAY ĐỔI URL Ở ĐÂY
    # ⚠️ CHỈ DÙNG WEBSITE BẠN SỞ HỮU HOẶC ĐƯỢC PHÉP TEST
    
    target_url = "https://httpbin.org/get"  # Website test an toàn
    # target_url = "https://jsonplaceholder.typicode.com/posts"  # Hoặc dùng cái này
    # target_url = "https://example.com"  # THAY URL CỦA BẠN Ở ĐÂY
    
    print("="*60)
    print("WEB STRESS TEST - TERMUX")
    print("="*60)
    print(f"Target: {target_url}")
    print("Requests: 50")
    print("Concurrency: 10")
    print("="*60)
    
    # Tạo tester với cấu hình nhẹ cho Termux
    tester = AdvancedWebStressTester(
        target_url=target_url,
        num_requests=50,      # Bắt đầu với số nhỏ
        concurrency=10,       # Đồng thời thấp
        use_proxy=False,      # Không dùng proxy
        proxy_file=None,      # Không có file proxy
        attack_mode="mixed"   # Chế độ hỗn hợp
    )
    
    # Chạy test
    tester.run()
    
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Kiểm tra file stress_test.py có trong thư mục không")
    print("Thư mục hiện tại:", os.getcwd())
    print("Files trong thư mục:", os.listdir('.'))
except Exception as e:
    print(f"Lỗi: {e}")
