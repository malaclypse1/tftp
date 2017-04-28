import socket
import select
import tftp
import argparse
import sys

def txfile(ip, port, filename, mode):
    # send data packet to client
    # wait for ack of the correct block
    # send next data packet
    # if incorrect ack received, do nothing
    # if other type of packet received send error Packet
    # wait for ack (block # should be last block received)
    
    print("ip: {} {} file: {} mode: {}".format(ip, port,
          filename, mode))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port+1))

    f = open(filename,"rb")
    opcode = 3
    block = 1
    done = False
    #send data until packet size < 512
    while (not done):
        #read portion of file
        data = f.read(512)
        #if portion is smaller than 508, its the last block
        if (sys.getsizeof(data) < 512):
            done = True
        #prepend opcode and block number
        data = (opcode.to_bytes (2,byteorder='big')
               + block.to_bytes (2,byteorder='big')
               + data)
        #send block
        acknowledged = False
        while (not acknowledged):
            sock.sendto(data, (ip, port))
            #wait for ack
            ackData, addr = sock.recvfrom(516)
            ackPack = tftp.Packet(ackData)
            if (ackPack.opcode == 4 and ackPack.block == block):
                #ack received
                block += 1
                acknowledged = True
            #else resend

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
