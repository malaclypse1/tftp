
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

    def __init__(self, raw):
        self.opcode, rest = int.from_bytes(raw[:2],byteorder='big'),raw[2:]
        if self.opcode == 1 or self.opcode == 2:
            self.filename, self.mode, devnull = rest.decode('ascii').split('\x00',2)
        elif self.opcode == 3:
            self.data = rest
        elif self.opcode == 4:
            self.block = int.from_bytes(rest,byteorder='big')
        elif self.opcode == 5:
            self.errorCode,rest = int.from_bytes(rest[:2],byteorder='big'),rest[2:]
            self.errMsg, devnull = rest.decode('ascii').split('\x00',1)
        else:
            raise ValueError('Invalid opcode')

    def __str__(self):
        returnStr = self.opstr[self.opcode]
        if self.opcode == 1 or self.opcode == 2:
            returnStr += ' filename: ' + self.filename + ' mode: ' + self.mode
        elif self.opcode == 3:
            returnStr += ' data:\n' + self.data.decode('ascii')
        elif self.opcode == 4:
            returnStr += ' block #' + str(self.block)
        elif self.opcode == 5:
            returnStr += ' error ' + str(self.errorCode) + ': ' + self.errMsg
        return returnStr
