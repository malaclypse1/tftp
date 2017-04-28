import socket
import select
import tftp
import random
import sys

def txfile(ip, ctid, filename, mode):
    # send data packet to client
    # wait for ack of the correct block
    # send next data packet
    # if incorrect ack received, do nothing
    # if other type of packet received send error Packet
    # wait for ack (block # should be last block received)
    
    print("ip: {} {} file: {} mode: {}".format(ip, ctid,
          filename, mode))
    stid = random.randint(2000,65535)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, stid))

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
        datapack = tftp.Packet()
        datapack.makeDATA(block,data)
#         data = (opcode.to_bytes (2,byteorder='big')
#                + block.to_bytes (2,byteorder='big')
#                + data)
        #send block
        acknowledged = False
        while (not acknowledged):
            sock.sendto(datapack.raw, (ip, ctid))
            print("sending block {}".format(block))
            #wait for ack
            ackData, addr = sock.recvfrom(516)
            ackPack = tftp.Packet()
            ackPack.decode(ackData)
            print(ackPack)
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
    pack = tftp.Packet()
    pack.decode(data)
    print(pack)
    if pack.opcode == 1: # request for file
        txfile(addr[0], addr[1], pack.filename, pack.mode)