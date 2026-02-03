#!/bin/bash
clear
echo "=========================================="
echo "    WEB STRESS TEST - SIMPLE VERSION"
echo "=========================================="
echo ""
echo "⚠️  CẢNH BÁO: CHỈ TEST WEBSITE ĐƯỢC PHÉP!"
echo ""
read -p "🌐 Nhập URL mục tiêu: " url
read -p "📊 Số requests (mặc định 1000): " req
read -p "⚡ Số threads (mặc định 20): " threads
read -p "🎯 Chế độ [mixed/database/ssl/session] (mặc định mixed): " mode

# Set defaults if empty
req=${req:-1000}
threads=${threads:-20}
mode=${mode:-mixed}

echo ""
echo "=========================================="
echo "CẤU HÌNH:"
echo "URL: $url"
echo "Requests: $req"
echo "Threads: $threads"
echo "Mode: $mode"
echo "=========================================="
echo ""
read -p "Bắt đầu test? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    cd ~/web-test
    python3 -c "
import sys
sys.path.append('.')
from stress_test import AdvancedWebStressTester

tester = AdvancedWebStressTester(
    target_url='$url',
    num_requests=$req,
    concurrency=$threads,
    use_proxy=False,
    proxy_file=None,
    attack_mode='$mode'
)

tester.run()
"
else
    echo "❌ Đã hủy!"
fi
