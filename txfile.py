import socket
import tftp
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("ip")
parser.add_argument("port", type=int)
parser.add_argument("filename", type=str)
parser.add_argument("mode", type=str)
args = parser.parse_args()
print("ip: {} {} file: {} mode: {}".format(args.ip, args.port, args.filename, args.mode))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((args.ip, args.port+1))

f = open(args.filename,"rb")
opcode = 3
block = 1
done = False
#send data until packet size < 512
while (not done):
    #read portion of file
    data = f.read(508)
    #if portion is smaller than 508, its the last block
    if (sys.getsizeof(data) < 508):
        done = True
    #prepend opcode and block number
    data = (opcode.to_bytes (2,byteorder='big')
           + block.to_bytes (2,byteorder='big')
           + data)
    #send block
    acknowledged = False
    while (not acknowledged):
        sock.sendto(data, (args.ip, args.port))
        #wait for ack
        ackData, addr = sock.recvfrom(512)
        ackPack = tftp.Packet(ackData)
        if (ackPack.opcode == 4 and ackPack.block == block):
            #ack received
            block += 1
            acknowledged = True
        #else resend
