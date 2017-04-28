
class Packet:
    """A TFTP Packet consists of a 2 byte opcode followed by opcode specific fields
    opcode  operation   remainder of packet
    1       RRQ         string Filename, null, string Mode, null
    2       WRQ          "
    3       DATA        2 byte block #, n bytes data
    4       ACK         2 byte block #
    5       ERROR       2 byte ErrorCode, string ErrMsg, null"""

    opstr = {1:"RRQ",
             2:"WRQ",
             3:"DATA",
             4:"ACK",
             5:"ERROR",
    }
    # new Packet object needs a place to store raw bytes
    def __init__(cls, raw=False):
        cls.raw = raw
        
    # raw bytes (like an rxed packet) can be added to the packet in the constructor:
    #   p1 = tftp.Packet(rawBytes)
    #   p1.decode()
    # or in the decoder:
    #   p1 = tftp.Packet()
    #   p1.decode(rawBytes)
    
    @classmethod
    def decode(cls, raw=False):
        if raw:
            cls.raw = raw
        if not cls.raw:
            raise ValueError('Can not decode empty Packet')
        cls.opcode, rest = int.from_bytes(cls.raw[:2],byteorder='big'),cls.raw[2:]
        if cls.opcode == 1 or cls.opcode == 2:
            cls.filename, cls.mode, devnull = rest.decode('ascii').split('\x00',2)
        elif cls.opcode == 3:
            cls.data = rest
        elif cls.opcode == 4:
            cls.block = int.from_bytes(rest,byteorder='big')
        elif cls.opcode == 5:
            cls.errorCode,rest = int.from_bytes(rest[:2],byteorder='big'),rest[2:]
            cls.errMsg, devnull = rest.decode('ascii').split('\x00',1)
        else:
            raise ValueError('Invalid opcode')
        return cls.opcode
            
    @classmethod
    def makeRQ(cls, opcode, filename, mode):
        cls.opcode = opcode
        cls.filename = filename
        cls.mode = mode # add valid mode checking <----------
        cls.raw = (opcode.to_bytes(2, byteorder='big')
                   + filename
                   + b'\x00'
                   + mode
                   + b'\x00')
        return cls.raw
    
    @classmethod
    def makeRRQ(cls, filename, mode):
        return makeRQ(1, filename, mode)
    
    @classmethod
    def makeWRQ(cls, filename, mode):
        return makeRQ(2, filename, mode)
    
    @classmethod
    def makeDATA(cls, block, data):
        cls.opcode = 3
        cls.block = block
        cls.data = data
        cls.raw = (opcode.to_bytes(2, byteorder='big')
                   + block.to_bytes(2, byteorder='big')
                   + data) # do something regarding mode netascii or octet? <-------
        return cls.raw
    
    @classmethod
    def makeACK(cls, block):
        cls.opcode = 4
        cls.block = block
        cls.raw = (opcode.to_bytes(2, byteorder='big')
                   + block.to_bytes(2, byteorder='big'))
        return cls.raw
    
    @classmethod
    def makeERROR(cls, errorCode, errMsg):
        cls.opcode = 5
        cls.errorCode = errorCode
        cls.errMsg = errMsg
        cls.raw = (opcode.to_bytes(2, byteorder='big')
                   + errorCode.to_bytes(2, byteorder='big')
                   + errMsg
                   + b'\x00')
        return cls.raw
    
    @classmethod
    def __str__(cls):
        try:
            cls.opcode
        except AttributeError:
            raise AttributeError('No opcode -- packet empty or not decoded')
        returnStr = cls.opstr[cls.opcode]
        if cls.opcode == 1 or cls.opcode == 2:
            returnStr += ' filename: ' + cls.filename + ' mode: ' + cls.mode
        elif cls.opcode == 3:
            returnStr += ' data:\n' + cls.data.decode('ascii')
        elif cls.opcode == 4:
            returnStr += ' block #' + str(cls.block)
        elif cls.opcode == 5:
            returnStr += ' error ' + str(cls.errorCode) + ': ' + cls.errMsg
        return returnStr
