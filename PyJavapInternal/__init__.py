__author__ = 'jasonlee'

def ByteToHex(byteStr):

    return ''.join(["%02X" % ord(x) for x in byteStr])

def HexToByte(hexStr):

    bytes = []


