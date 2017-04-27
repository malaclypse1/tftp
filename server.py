import socket
import select
import tftp

# Simple TFTP server
####################
# This program will listen on port 69 for incoming tftp requests
# On receiving a request, it will randomly select a TID and reply
# appropriately
# hand off file transfers to txfile.py or rxfile.py

UDP_IP = ""
UDP_PORT = 1069

listenSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listenSock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = listenSock.recvfrom(512)
    print("received from {}: {}".format(addr, data))
    pack = tftp.Packet(data)
    print(pack)
